import json
import requests
import pprint
from requests.auth import HTTPBasicAuth

def get_repos_by_username(parametros):
    request_headers = {"Content-type" : "application/json"}
    request_url = parametros["url_base_github"]+"users/"+parametros["username_repo"]+"/repos"
    request = requests.get(url=request_url, headers=request_headers, auth=(parametros["username_github"], parametros["password_github"]))
    repos = request.json()
    # pprint.pprint(membership)
    return repos
#
# def get_commits_by_reponame(parametros):
#     request_headers = {"Content-type" : "application/json"}
#     request_url = parametros["url_base_github"]+"repos/"+parametros["username"]+"/"+parametros["reponame"]+"/commits"
#     request = requests.get(url=request_url, headers=request_headers)
#     commits = request.json()
#     # pprint.pprint(membership)
#     return commits

def get_commits_by_reponame(parametros, reponame):
    request_headers = {"Content-type" : "application/json"}
    request_url = parametros["url_base_github"]+"repos/"+parametros["username_repo"]+"/"+reponame+"/commits"
    request_params = {}
    for criteria in ["since", "until", "sha", "author", "path"]:
        if criteria in parametros:
            request_params[criteria] = parametros[criteria]

    request = requests.get(url=request_url, headers=request_headers, params=request_params, auth=(parametros["username_github"], parametros["password_github"]))
    commits = request.json()
    # pprint.pprint(membership)
    return commits
