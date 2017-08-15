import json
import requests
import pprint

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
    request_url = parametros["url_base"]+"users/"+str(parametros["user_data"]["user_id"])+"/membership?limit=-1"
    request = requests.get(url=request_url, headers=request_headers)
    membership = request.json()
    # pprint.pprint(membership)
    return membership

def get_trackers_tuleap(parametros, project_id):
    request_headers = {"Content-type" : "application/json",
    "X-Auth-Token":str(parametros["user_data"]["token"]),
    "X-Auth-UserId":str(parametros["user_data"]["user_id"])}
    request_url = parametros["url_base"]+"projects/"+str(project_id)+"/trackers?limit=-1"
    # requests_params = {"shortname":project_shortname}
    request = requests.get(url=request_url, headers=request_headers)
    project_trackers = request.json()
    # pprint.pprint(project_trackers)
    return project_trackers

def get_project_info_tuleap(parametros, project_shortname):
    request_headers = {"Content-type" : "application/json",
    "X-Auth-Token":str(parametros["user_data"]["token"]),
    "X-Auth-UserId":str(parametros["user_data"]["user_id"])}
    request_url = parametros["url_base"]+"projects?query=%7B%22shortname%22%3A%22"+str(project_shortname)+"%22%7D"
    # requests_params = {"shortname":project_shortname}
    request = requests.get(url=request_url, headers=request_headers)
    project_info = request.json()
    # pprint.pprint(project_info)
    return project_info

def send_comment_tuleap(parametros, comentario, tracker_id):
    payload = {}
    payload.type = "text"
    payload.body = comentario
    request_headers = {"Content-type" : "application/json",
    "X-Auth-Token":str(parametros["user_data"]["token"]),
    "X-Auth-UserId":str(parametros["user_data"]["user_id"])}
    request_url = parametros["url_base"]+"artifacts/"+str(tracker_id)
    # requests_params = {"shortname":project_shortname}
    request = requests.put(url=request_url, headers=request_headers, data=json.dumps(payload))
    # pprint.pprint(project_info)
    return request.status_code
