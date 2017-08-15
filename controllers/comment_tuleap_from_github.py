
import tuleap_api
import github_api
# from github import Github
import pprint

def comment_tuleap_from_github_func(parametros):
    parametros["url_base"]="https://api.github.com/"

    repos = github_api.get_repos_by_username(parametros)
    pprint.pprint(repos)
    for repo in repos:
        commits = github_api.get_commits_by_reponame(parametros, repo["name"])
        for commit_info in commits:
            if "commit" in commit_info:
                pprint.pprint(commit_info["commit"])
            else:
                print "Not Found\n"
        # break
    # user_data = tuleap_api..autenticar_tuleap(parametros)
    # parametros["user_data"] = user_data




    return None
