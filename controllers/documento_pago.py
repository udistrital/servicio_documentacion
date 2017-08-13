import json
import requests
import pprint

def generar_documento_pago(parametros):
    parametros["url_base"]="https://tuleap.udistrital.edu.co/api/"
    user_data = autenticar_tuleap(parametros)
    parametros["user_data"] = user_data
    membership = get_membership(parametros)
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
    pprint.pprint(user_data)
    return user_data

def get_membership(parametros):
    request_headers = {"Content-type" : "application/json",
    "X-Auth-Token":str(parametros["user_data"]["token"]),
    "X-Auth-UserId":str(parametros["user_data"]["user_id"])}
    request_url = parametros["url_base"]+"users/"+str(parametros["user_data"]["user_id"])+"/membership"
    request = requests.get(url=request_url, headers=request_headers)
    membership = request.json()
    pprint.pprint(membership)
    return membership
