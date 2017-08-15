
import pprint
import tuleap_api

def generar_documento_pago(parametros):
    parametros["url_base"]="https://tuleap.udistrital.edu.co/api/"
    project_string_key = "_project"
    user_data = tuleap_api.autenticar_tuleap(parametros)
    parametros["user_data"] = user_data
    membership = tuleap_api.get_membership_tuleap(parametros)
    project_shortname_cache = []
    project_member_info = []
    for project_membership in membership:
        project_shortname = project_membership[:project_membership.find(project_string_key)]
        # print "Proyecto "+project_shortname
        if not any(project_shortname in s for s in project_shortname_cache):
            project_shortname_cache.append(project_shortname)
            project_info = tuleap_api.get_project_info_tuleap(parametros, project_shortname)
            if len(project_info) > 0:
                project_member_info.append(project_info[0])
    # pprint.pprint(project_member_info)
    for project in project_member_info:
        pprint.pprint(tuleap_api.get_trackers_tuleap(parametros, project["id"]))
    return None
