import csv
import os
from utils.utils import format_date

# Função para salvar os repositórios em um CSV
def save_repo_info_to_csv(repos, filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, filename)
    
    headers = [
        "Index", "Nome do Repositório", "URL", "Total de Estrelas", "Data de Criação", "Total de PRs"
    ]

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for index, repo in enumerate(repos, start=1):
            repo_name = repo["name"]
            repo_url = repo["url"]
            repo_stars = repo["stargazerCount"]
            repo_creation_date = format_date(repo["createdAt"])
            repo_total_prs = repo["pullRequests"]["totalCount"]
            
            writer.writerow([index, repo_name, repo_url, repo_stars, repo_creation_date, repo_total_prs])

# Função para salvar PRs em um CSV
def save_pr_info_to_csv(prs, filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, filename)
    
    headers = [
        "Index", "Título do PR", "URL", "Data de Criação", "Data de Fechamento", 
        "Total de Revisões", "Decisão da Revisão", "Total de Adições", 
        "Total de Remoções", "Total de Arquivos Alterados", "Comprimento da Descrição", 
        "Tempo de Análise (horas)", "Total de Comentários", "Total de Participantes"
    ]

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for index, pr in enumerate(prs, start=1):
            pr_title = pr["title"]
            pr_url = pr["url"]
            pr_creation_date = format_date(pr["createdAt"])
            pr_closed_date = format_date(pr["mergedAt"] or pr["closedAt"])
            pr_reviews = pr["reviews"]["totalCount"]
            pr_review_decision = pr["reviewDecision"]
            pr_additions = pr["additions"]
            pr_deletions = pr["deletions"]
            pr_changed_files = pr["changedFiles"]
            pr_description_length = pr["description_length"]
            pr_analysis_time = pr["analysis_time"]
            pr_comments = pr["comments_count"]
            pr_participants = pr["participants_count"]
            
            writer.writerow([
                index, pr_title, pr_url, pr_creation_date, pr_closed_date, 
                pr_reviews, pr_review_decision, pr_additions, pr_deletions, 
                pr_changed_files, pr_description_length, pr_analysis_time, 
                pr_comments, pr_participants
            ])
