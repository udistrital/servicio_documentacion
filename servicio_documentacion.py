from flask import Flask, render_template, request, jsonify, make_response
from controllers import documento_pago, numero_a_letras
from flask_api import status
import pprint
import sys
import requests
import json
import pdfkit
import glob, os

ruta_archivos="/srv/http/documentos_mensuales/"
ruta_servicios="http://127.0.0.1:5000/"

app = Flask(__name__)
app.jinja_env.globals.update(valor_letras=numero_a_letras.numero_a_letras) 

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
def generar_cumplido_masivo():

	with open('datos_temp/base_datos_oas.json') as data_file:
		data = json.load(data_file)
	
	for contratista in data["contratistas"]:
		pprint.pprint(contratista)
		generar_cumplido_individual(contratista["id"])

	return "Generación exitosa", status.HTTP_200_OK

@app.route('/documento_mensual/cumplido/<string:identificacion>', methods=['GET'])
def get_generar_cumplido_individual():
	if generar_cumplido_individual(identificacion):
		return "Generación exitosa", status.HTTP_200_OK
	else:
		return "Error", HTTP_406_NOT_ACCEPTABLE

@app.route('/datos_informe', methods=['GET'])
def get_datos_informe():
	return jsonify(datos_informe())



@app.route('/datos_contratista/<string:identificacion>', methods=['GET'])
def get_datos_contratista():
	try:
		return jsonify(datos_contratista(identificacion))
	except:
		return jsonify({})

@app.route('/documento_mensual/cumplido_pdf', methods=['POST'])
def get_html_to_pdf_masivo():
	parametros = None
	try:
		parametros = request.get_json(force = True)
		#pprint.pprint(parametros)
	except:
		print()
	if parametros:
		html_to_pdf_masivo(ruta_archivos+parametros["tipo"]+"/"+parametros["vigencia"]+"/"+parametros["mes"]+"")
		return "Generación exitosa", status.HTTP_200_OK 

def html_to_pdf_masivo(ruta):
	os.chdir(ruta)
	for file in glob.glob("*.html"):
		html_to_pdf(os.path.join(ruta,file),os.path.join(ruta,"pdf",file+".pdf"))


def html_to_pdf(path_html, path_pdf, options = None):
	if not options:
		options = {
		'page-size': 'Letter',
		'encoding': "UTF-8",
		'no-outline': None,
		'orientation': 'Portrait'
		}
	print("Ruta "+path_html)
	print("PDF  "+path_pdf)
	pdfkit.from_file(path_html, path_pdf, options=options)

def datos_informe():
	informe_data = {}
	informe_data["dia_inicial"]="01"
	informe_data["dia_final"]="30"
	informe_data["mes"]="septiembre"
	informe_data["vigencia"]="2017"
	informe_data["dia_informe"]=29

	jefe_data={}
	jefe_data["nombre_completo"]="Beatriz Jaramillo"
	jefe_data["cargo"]="Jefe Asesora de Sistemas"
	print("Datos informe")
	return {"informe":informe_data,"jefe":jefe_data}

def generar_cumplido_individual(identificacion):
	print("Individual de "+identificacion)
	usuario_data = datos_contratista(identificacion)
	informe_data = datos_informe()
	pprint.pprint(informe_data)
	fname = ruta_archivos+"cumplido/"+informe_data["informe"]["vigencia"]+"/"+informe_data["informe"]["mes"]+"/"+str(identificacion)+".html"
	print("Ruta: "+fname)
	with open(fname, 'w') as f:
		html = render_template('cumplido/template_cumplido.html', usuario=usuario_data, jefe=informe_data["jefe"], informe=informe_data["informe"])
		f.write(html)
	return True

def datos_contratista(identificacion):
	print("Datos contratista "+identificacion)
	with open('datos_temp/base_datos_contratista.json') as data_file:    
		data = json.load(data_file)
	
	try:
		return data[identificacion]
	except:
		return {}

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
