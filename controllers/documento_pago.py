import json
import requests
import pprint

def generar_documento_pago(parametros):
    parametros["url_base"]="https://tuleap.udistrital.edu.co/api/"
    project_string_key = "_project"
    user_data = autenticar_tuleap(parametros)
    parametros["user_data"] = user_data
    membership = get_membership_tuleap(parametros)
    project_shortname_cache = []

    for project_membership in membership:
        project_shortname = project_membership[:project_membership.find(project_string_key)]
        # print "Proyecto "+project_shortname
        if not any(project_shortname in s for s in project_shortname_cache):
            project_shortname_cache.append(project_shortname)
            project_info = get_project_info_tuleap(parametros, project_shortname)
            if len(project_info) > 0:
                project_info = project_info[0]
            pprint.pprint(project_info)
    # user_id = response+["user_id"]
    # token   = response["token"]
    # uri     = response["uri"]

    return None

def autenticar_tuleap(parametros):
    request_headers = {"Content-type" : "application/json"}
    request_data = {"username" : parametros["username"], "password" : parametros["password"]}
    request_url = parametros["url_base"]+"tokens"
    request = requests.post(url=request_url, json=request_data, headers=request_headers)
    user_data = request.json()
    # pprint.pprint(user_data)
    return user_data

def get_membership_tuleap(parametros):
    request_headers = {"Content-type" : "application/json",
    "X-Auth-Token":str(parametros["user_data"]["token"]),
    "X-Auth-UserId":str(parametros["user_data"]["user_id"])}
    request_url = parametros["url_base"]+"users/"+str(parametros["user_data"]["user_id"])+"/membership"
    request = requests.get(url=request_url, headers=request_headers)
    membership = request.json()
    # pprint.pprint(membership)
    return membership

def get_trackers_tuleap(parametros):

    return None

def get_project_info_tuleap(parametros, project_shortname):
    request_headers = {"Content-type" : "application/json",
    "X-Auth-Token":str(parametros["user_data"]["token"]),
    "X-Auth-UserId":str(parametros["user_data"]["user_id"])}
    request_url = parametros["url_base"]+"projects?query=%7B%22shortname%22%3A%22"+project_shortname+"%22%7D"
    # requests_params = {"shortname":project_shortname}
    request = requests.get(url=request_url, headers=request_headers)
    project_info = request.json()
    # pprint.pprint(project_info)
    return project_info
