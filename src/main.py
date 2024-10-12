import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Autenticação
personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')

headers = {
    "Authorization": f"Bearer {personal_access_token}",
    "Content-Type": "application/json"
}

# Função para verificar rate limit da API
def check_rate_limit():
    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    rate_limit = response.json()['rate']['remaining']
    print(f"Requests remaining: {rate_limit}")
    return rate_limit

# Função para fazer a requisição GraphQL com tentativas
def run_query(query, retries=8):
    for attempt in range(retries):
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            print(f"Attempt {attempt + 1} failed with status code {request.status_code}. Retrying...")
            time.sleep(5)
    raise Exception(f"Query failed to run after {retries} attempts. Last status code: {request.status_code}. {query}")

# Função para obter repositórios populares com paginação
def get_repos():
    repos_data = []
    has_next_page = True
    cursor = None
    index = 1

    while has_next_page and len(repos_data) < 100:  # Limite de 60 repositórios
        query_repos = f"""
        {{
          search(query: "stars:>100", type: REPOSITORY, first: 10{' after: "' + cursor + '"' if cursor else ''}) {{
            edges {{
              cursor
              node {{
                ... on Repository {{
                  name
                  url
                  stargazerCount
                  createdAt
                  pullRequests(states: [MERGED, CLOSED]) {{
                    totalCount
                  }}
                }}
              }}
            }}
            pageInfo {{
              hasNextPage
              endCursor
            }}
          }}
        }}
        """

        result = run_query(query_repos)
        
        for repo in result['data']['search']['edges']:
            node = repo['node']
            if node['pullRequests']['totalCount'] >= 100:  # Filtro de PRs
                repos_data.append([
                    index,
                    node['name'],
                    node['url'],
                    node['stargazerCount'],
                    node['createdAt'],
                    node['pullRequests']['totalCount']
                ])
                index += 1
        
        # Atualizando os dados de paginação
        has_next_page = result['data']['search']['pageInfo']['hasNextPage']
        cursor = result['data']['search']['pageInfo']['endCursor']
        time.sleep(10)  # Pausa maior entre requisições para evitar rate limits
    
    return repos_data

# Salvando os dados de repositórios em CSV
def save_repos_to_csv(repos_data):
    df = pd.DataFrame(repos_data, columns=[
        "Index", "Nome do Repositório", "URL", "Total de Estrelas", "Data de Criação", "Total de PRs"])
    df.to_csv('repos_infos_paginated.csv', index=False)

# Consulta para obter os PRs
def get_prs(owner, repo_name):
    query_prs = f"""
    {{
      repository(owner: "{owner}", name: "{repo_name}") {{
        pullRequests(first: 50, states: [MERGED, CLOSED]) {{
          edges {{
            node {{
              title
              url
              createdAt
              closedAt
              additions
              deletions
              changedFiles
              body
              reviews {{
                totalCount
              }}
              comments {{
                totalCount
              }}
              participants {{
                totalCount
              }}
            }}
          }}
        }}
      }}
    }}
    """
    result = run_query(query_prs)
    prs_data = []
    index = 1
    
    if 'data' not in result or 'repository' not in result['data'] or 'pullRequests' not in result['data']['repository']:
        print(f"No pull request data found for {repo_name}.")
        return prs_data
    
    for pr in result['data']['repository']['pullRequests']['edges']:
        pr_node = pr['node']
        
        # Calculando o tempo de análise em horas
        created_at = pd.to_datetime(pr_node['createdAt'])
        closed_at = pd.to_datetime(pr_node['closedAt'])
        analysis_time = (closed_at - created_at).total_seconds() / 3600  # em horas
        
        # Verificando se o PR tem pelo menos uma revisão
        if pr_node['reviews']['totalCount'] > 0 and analysis_time > 1:
            prs_data.append([
                index,
                pr_node['title'],
                pr_node['url'],
                pr_node['createdAt'],
                pr_node['closedAt'],
                pr_node['reviews']['totalCount'],
                'MERGED' if pr_node['closedAt'] else 'CLOSED',
                pr_node['additions'],
                pr_node['deletions'],
                pr_node['changedFiles'],
                len(pr_node['body']) if pr_node['body'] else 0,
                analysis_time,
                pr_node['comments']['totalCount'],
                pr_node['participants']['totalCount']
            ])
            index += 1
        else:
            print(f"PR '{pr_node['title']}' was skipped (no reviews or analysis time < 1 hour).")
    
    if len(prs_data) == 0:
        print(f"No PRs were found for repository {repo_name}.")
    
    return prs_data

# Salvando os dados de PRs em CSV
def save_prs_to_csv(prs_data):
    df = pd.DataFrame(prs_data, columns=[
        "Index", "Título do PR", "URL", "Data de Criação", "Data de Fechamento", "Total de Revisões",
        "Decisão da Revisão", "Total de Adições", "Total de Remoções", "Total de Arquivos Alterados",
        "Comprimento da Descrição", "Tempo de Análise (horas)", "Total de Comentários", "Total de Participantes"
    ])
    df.to_csv('prs_infos_paginated.csv', index=False)

# Função principal
if __name__ == "__main__":
    # Verificar limite de rate antes de iniciar
    check_rate_limit()

    # Passo 1: Obtenção de repositórios
    repos_data = get_repos()
    save_repos_to_csv(repos_data)
    
    # Passo 2: Obtenção de PRs para cada repositório
    all_prs_data = []
    for repo in repos_data:
        repo_url_parts = repo[2].split('/')[-2:]  # Usar a URL correta do repositório (repo[2])
        repo_owner, repo_name = repo_url_parts[0], repo_url_parts[1]
        prs_data = get_prs(repo_owner, repo_name)
        if prs_data:
            all_prs_data.extend(prs_data)
        else:
            print(f"No PR data found for repository: {repo_name}")
        time.sleep(3)  # Pausa maior entre requisições para evitar rate limits
    
    # Salvando todos os dados de PRs em CSV
    if all_prs_data:
        save_prs_to_csv(all_prs_data)
    else:
        print("No PR data collected.")
