from flask import Flask, render_template, request, jsonify
from controllers import documento_pago
from flask_api import status
import pprint

app = Flask(__name__)


@app.route('/documento_mensual/informe_gestion', methods=['POST'])
def generar_informe_gestion():
	try:
		parametros = request.get_json(force = True)
		#pprint.pprint(parametros)
		actividades = documento_pago.generar_documento_pago(parametros)
		#pprint.pprint(actividades)
	except:
		actividades = None
	usuario_data = {}
	usuario_data['contrato'] = {}
	usuario_data['contrato']['objeto'] = """Actuar como desarrollador junior de soluciones informáticas 
	que soportan procesos los académicos /administrativos institucionales, ciñéndose al modelo de gestión
	 y evaluación de necesidades y requerimientos utilizado por la Oficina Asesora de Sistemas y el método 
	 de desarrollo institucional OPENUP/OAS para la ejecución la segunda (II) etapa de la fase de 
	 construcción del Proyecto ECOSIIS (PMIT-PE15) - Sistema de Gestión Financiera"""

	usuario_data["rotulo"]="Sr"
	usuario_data["nombre_completo"]="Fabio Andres Parra Fuentes"
	usuario_data["dia_inicial"]="01"
	usuario_data["dia_final"]="30"
	usuario_data["mes"]="Agosto"

	usuario_data["documento"]={}
	usuario_data["documento"]["tipo"]="Cedula de Ciudadania"
	usuario_data["documento"]["numero"]="1030577784"
	usuario_data["documento"]["ciudad"]="Bogota"

	usuario_data["valor_mensual"]={}
	usuario_data["valor_mensual"]["formato_letras"]="Valor en letras"
	usuario_data["valor_mensual"]["formato_moneda"]="3579000"
	
	usuario_data["cuenta"]={}
	usuario_data["cuenta"]["tipo"]="Ahorros"
	usuario_data["cuenta"]["numero"]="692-111222-87"
	usuario_data["cuenta"]["banco"]="Bancolombia"
	if actividades:
		return jsonify(actividades)
	try:
		return render_template('informe_gestion/template_informe_gestion.html',usuario=usuario_data)
	except:
		return "No generado", status.HTTP_404_NOT_FOUND


@app.route('/documento_mensual/cumplido', methods=['GET'])
def generar_cumplido():
	#parametros = request.get_json()
	usuario_data = {}
	usuario_data["rotulo"]="Sr"
	usuario_data["nombre_completo"]="Fabio Andres Parra Fuentes"
	usuario_data["dia_inicial"]="01"
	usuario_data["dia_final"]="30"
	usuario_data["mes"]="Agosto"

	usuario_data["documento"]={}
	usuario_data["documento"]["tipo"]="Cedula de Ciudadania"
	usuario_data["documento"]["numero"]="1030577784"
	usuario_data["documento"]["ciudad"]="Bogota"

	usuario_data["valor_mensual"]={}
	usuario_data["valor_mensual"]["formato_letras"]="Valor en letras"
	usuario_data["valor_mensual"]["formato_moneda"]="3579000"
	
	usuario_data["cuenta"]={}
	usuario_data["cuenta"]["tipo"]="Ahorros"
	usuario_data["cuenta"]["numero"]="692-111222-87"
	usuario_data["cuenta"]["banco"]="Bancolombia"

	jefe_data={}
	jefe_data["nombre_completo"]="Beatriz Algo"
	jefe_data["cargo"]="Jefe Asesora de Sistemas"

	try:
		return render_template('cumplido/template_cumplido.html', usuario=usuario_data, jefe=jefe_data)
	except:
		return "No generado", status.HTTP_404_NOT_FOUND


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
