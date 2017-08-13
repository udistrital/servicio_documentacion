import json
import requests
import pprint

def generar_documento_pago(parametros):

    request_headers = {"Content-type" : "application/json"}
    request_data = {"username" : parametros["username"], "password" : parametros["password"]}
    request_url = "https://tuleap.udistrital.edu.co/api/tokens"
    request = requests.post(url=request_url, json=request_data, headers=request_headers)
    user_data = request.json()
    pprint.pprint(user_data)

    # user_id = response+["user_id"]
    # token   = response["token"]
    # uri     = response["uri"]

    return None
