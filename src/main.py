import requests
from dotenv import load_dotenv
import time
import os
from utils.utils import calculate_time_difference_in_hours
from utils.dataSaver import save_repo_info_to_csv, save_pr_info_to_csv
from concurrent.futures import ThreadPoolExecutor

load_dotenv('.env')

personal_access_token = os.getenv('PERSONAL_ACCESS_TOKEN')
github_graphQl_api_url = "https://api.github.com/graphql"

# Função para monitorar os limites de taxa da API
def check_rate_limit():
    headers = {
        "Authorization": f"Bearer {personal_access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get("https://api.github.com/rate_limit", headers=headers)
    rate_limits = response.json()
    
    remaining = rate_limits['rate']['remaining']
    reset_time = rate_limits['rate']['reset']  # Timestamp when the limit será resetado
    
    if remaining == 0:
        current_time = time.time()
        sleep_time = reset_time - current_time
        if sleep_time > 0:
            print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
    else:
        print(f"Rate limit remaining: {remaining}")

# Função para realizar chamada à API GraphQL do GitHub com monitoramento de limites
def run_graphql_query(query, variables=None):
    headers = {
        "Authorization": f"Bearer {personal_access_token}",
        "Content-Type": "application/json"
    }

    json = {"query": query, "variables": variables}

    retry_attempts = 3
    for attempt in range(retry_attempts):
        check_rate_limit()  # Verifica o limite de taxa antes de cada chamada
        response = requests.post(github_graphQl_api_url, json=json, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if "errors" in result:
                raise Exception(f"Erro no GraphQL: {result['errors']}")
            return result["data"]
        elif response.status_code == 502 and attempt < retry_attempts - 1:
            print(f"Retrying due to 502 error (attempt {attempt + 1})...")
            time.sleep(10)  # Aumenta o tempo de espera para 10 segundos
        else:
            raise Exception(f"Erro ao executar a query: {response.status_code}, {response.text}")

# Função para buscar repositórios mais populares e que tenham pelo menos 100 PRs
def fetch_repos_with_prs(num_repos):
    query = """
    query($number_of_repos_per_request: Int!, $cursor: String) {
        search(query: "stars:>0", type: REPOSITORY, first: $number_of_repos_per_request, after: $cursor) {
            edges {
                node {
                    ... on Repository {
                        name
                        url
                        stargazerCount
                        createdAt
                        pullRequests(states: [MERGED, CLOSED]) {
                            totalCount
                        }
                    }
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
    """

    repos = []
    cursor = None

    while len(repos) < num_repos:
        variables = {"number_of_repos_per_request": 5, "cursor": cursor}
        result = run_graphql_query(query, variables)
        edges = result["search"]["edges"]

        for repo in edges:
            repo_node = repo["node"]
            # Verifica se o repositório tem pelo menos 100 PRs
            if repo_node["pullRequests"]["totalCount"] >= 100:
                repos.append(repo_node)

        if not result["search"]["pageInfo"]["hasNextPage"]:
            break

        cursor = result["search"]["pageInfo"]["endCursor"]
        time.sleep(5)  # Aumenta o tempo de espera entre as requisições para 5 segundos

    return repos[:num_repos]

# Função para obter PRs de um repositório com base nas condições
def fetch_pr_data(repo_name, repo_owner):
    query = """
    query($repo_owner: String!, $repo_name: String!, $cursor: String) {
        repository(owner: $repo_owner, name: $repo_name) {
            pullRequests(first: 50, after: $cursor, states: [MERGED, CLOSED]) {
                edges {
                    node {
                        title
                        url
                        createdAt
                        mergedAt
                        closedAt
                        reviews {
                            totalCount
                        }
                        reviewDecision
                        additions
                        deletions
                        changedFiles
                        body
                        comments {
                            totalCount
                        }
                        participants {
                            totalCount
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    }
    """

    pull_requests = []
    cursor = None

    while True:
        variables = {
            "repo_owner": repo_owner,
            "repo_name": repo_name,
            "cursor": cursor
        }
        result = run_graphql_query(query, variables)
        edges = result["repository"]["pullRequests"]["edges"]

        # Filtra PRs com pelo menos uma revisão e diferença de tempo maior que 1 hora
        for pull_request in edges:
            pr_node = pull_request["node"]
            if pr_node["reviews"]["totalCount"] > 0:
                merge_time = pr_node["mergedAt"] or pr_node["closedAt"]
                if merge_time and calculate_time_difference_in_hours(pr_node["createdAt"], merge_time) > 1:
                    # Calculando a descrição e o tempo de análise
                    description_length = len(pr_node["body"]) if pr_node["body"] else 0
                    analysis_time = calculate_time_difference_in_hours(pr_node["createdAt"], merge_time)

                    pr_data = {
                        "title": pr_node["title"],
                        "url": pr_node["url"],
                        "created_at": pr_node["createdAt"],
                        "merged_at": pr_node["mergedAt"],
                        "closed_at": pr_node["closedAt"],
                        "reviews_count": pr_node["reviews"]["totalCount"],
                        "review_decision": pr_node["reviewDecision"],
                        "additions": pr_node["additions"],
                        "deletions": pr_node["deletions"],
                        "changed_files": pr_node["changedFiles"],
                        "description_length": description_length,
                        "analysis_time": analysis_time,
                        "comments_count": pr_node["comments"]["totalCount"],
                        "participants_count": pr_node["participants"]["totalCount"]
                    }
                    pull_requests.append(pr_data)

        if not result["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]:
            break

        cursor = result["repository"]["pullRequests"]["pageInfo"]["endCursor"]
        time.sleep(5)  # Aumenta o tempo de espera entre as requisições para 5 segundos

    return pull_requests

# Função para paralelizar a coleta de PRs de cada repositório
def fetch_prs_for_repo(repo):
    repo_owner = repo["url"].split('/')[-2]
    repo_name = repo["name"]
    return fetch_pr_data(repo_name, repo_owner)

# Main
if __name__ == "__main__":
    # Número de repositórios mais populares que tenham mais de 100 PRs
    number_of_repos = 20
    try:
        # Buscar repositórios populares
        popular_repos = fetch_repos_with_prs(number_of_repos)
        save_repo_info_to_csv(popular_repos, "repos_info.csv")

        # Paralelizar a busca dos PRs
        with ThreadPoolExecutor(max_workers=5) as executor:
            all_prs = list(executor.map(fetch_prs_for_repo, popular_repos))                                                                                                                                                          

        # Salvar os dados de PRs coletados
        all_prs_data = [pr for repo_prs in all_prs for pr in repo_prs]  
        save_pr_info_to_csv(all_prs_data, "prs_info.csv")

    except Exception as e:
        print(e)
