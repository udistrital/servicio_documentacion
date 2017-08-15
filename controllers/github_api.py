import json
import requests
import pprint

def get_repos_by_username(parametros):
    request_headers = {"Content-type" : "application/json"}
    request_url = parametros["url_base"]+"users/"+parametros["username"]+"/repos"
    request = requests.get(url=request_url, headers=request_headers)
    repos = request.json()
    # pprint.pprint(membership)
    return repos
#
# def get_commits_by_reponame(parametros):
#     request_headers = {"Content-type" : "application/json"}
#     request_url = parametros["url_base"]+"repos/"+parametros["username"]+"/"+parametros["reponame"]+"/commits"
#     request = requests.get(url=request_url, headers=request_headers)
#     commits = request.json()
#     # pprint.pprint(membership)
#     return commits

def get_commits_by_reponame(parametros, reponame):
    request_headers = {"Content-type" : "application/json"}
    request_url = parametros["url_base"]+"repos/"+parametros["username"]+"/"+reponame+"/commits"

    for criteria in ["since", "until", "sha", "author", "path"]:
        if(parametros[criteria] != None):
            request_params[criteria] = parametros[criteria]

    request = requests.get(url=request_url, headers=request_headers, params=request_params)
    commits = request.json()
    # pprint.pprint(membership)
    return commits
