
import tuleap_api
import github_api
# from github import Github
import pprint
import re

def comment_tuleap_from_github_func(parametros):
    parametros["url_base_tuleap"]="https://tuleap.udistrital.edu.co/api/"
    user_data = tuleap_api.autenticar_tuleap(parametros)
    parametros["user_data"] = user_data
    pprint.pprint(user_data)
    parametros["url_base_github"]="https://api.github.com/"

    repos = github_api.get_repos_by_username(parametros)
    # pprint.pprint(repos)
    for repo in repos:
        commits = github_api.get_commits_by_reponame(parametros, repo["name"])
        for commit_info in commits:
            if "commit" in commit_info:
                task_regex_group = re.search('##(.+?) ', commit_info["commit"]["message"])
                if task_regex_group:
                    artifact_id = task_regex_group.group(1)
                    print "Artifact # --" + str(artifact_id)+"--"
                    print "Status "+str(tuleap_api.send_comment_tuleap(parametros, str(commit_info["commit"]["message"]), str(artifact_id)))
                else:
                    print "No hay tracker asociado"
                # pprint.pprint(commit_info["commit"]["message"])
            else:
                print "Not Found"
        # break
    # user_data = tuleap_api..autenticar_tuleap(parametros)
    # parametros["user_data"] = user_data




    return None
