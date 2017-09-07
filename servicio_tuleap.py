from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from controllers import tuleap_api, comment_tuleap_from_github
from controllers import text_tool, appconf
import re
app = Flask(__name__)
api = Api(app)

todos = {}
parametros = appconf.parametros
class TuleapService(Resource):
    def put(self, artifact_id):
        print(parametros)
        parametros["user_data"] = tuleap_api.autenticar_tuleap(parametros)
        hookGitData = request.get_json(force = True) 
        for commitInfo in hookGitData["commits"]:
            comment = text_tool.format_comment_by_expr(commitInfo["message"], '#(.+?)# ', '')
            if comment["artifact_id"]:
                artifact_id = comment["artifact_id"]
                print "Artifact # --" + str(artifact_id)+"--"
                print "Status "+str(tuleap_api.send_comment_tuleap(parametros, str(comment["message"]), str(artifact_id)))
            else:
                print "No hay Artifact asociado"
             
        return hookGitData["commits"]

api.add_resource(TuleapService, '/tuleapService/<string:artifact_id>')

if __name__ == '__main__':
    app.run(debug=True ,port=int(parametros["appport"]))