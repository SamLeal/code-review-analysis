        else:
            print(f"PR '{pr_node['title']}' was skipped (analysis time < 1 hour).")
    
    if len(prs_data) == 0:
        print(f"No PRs were found for repository {repo_name}.")