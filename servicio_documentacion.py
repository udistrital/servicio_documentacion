from flask import Flask, render_template, request, jsonify, make_response
from controllers import documento_pago, numero_a_letras, appconf
from flask_api import status
import pprint
import sys
import requests
import json
import pdfkit
import glob, os
import logging

ruta_archivos="/srv/http/documentos_mensuales/"
ruta_servicios="http://127.0.0.1:5000/"

# create logger
logger = logging.getLogger('Logger App')
level = logging.DEBUG
logger.setLevel(level)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(level)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

app = Flask(__name__)
app.jinja_env.globals.update(valor_letras=numero_a_letras.numero_a_letras) 
parametrosBase = appconf.parametros

@app.route('/documento_mensual/informe_gestion', methods=['POST'])
def generar_informe_gestion():

	try:
		parametros_body = request.get_json(force = True)
		logger.info("Body recuperado")
		logger.debug(pprint.pformat(parametros_body))
		parametros = parametros_body
		logger.debug("Parametros:")
		logger.debug(pprint.pformat(parametros))
		actividades = documento_pago.obtener_artefactos(parametros)
		logger.debug("Actividades:")
		logger.debug(pprint.pformat(actividades))
	except:
		logger.error("Error en obtencion de body")
		actividades = None

	if actividades:
		logger.info("Actividades enviadas")
		#return jsonify(actividades)
		usuario_data = datos_contratista("1030577784")
		#try:
		logger.info("Plantilla de gestion renderizada")
		return render_template('informe_gestion/template_informe_gestion.html',usuario=usuario_data, tamano_actividades=len(actividades), actividades=actividades)
		# except:
		# 	logger.error("Plantilla de gestion no renderizada")
		# 	return "No generado", status.HTTP_404_NOT_FOUND
	logger.error("Plantilla de gestion no renderizada")
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
def get_generar_cumplido_individual(identificacion):
	if generar_cumplido_individual(identificacion):
		return "Generación exitosa", status.HTTP_200_OK
	else:
		return "Error", HTTP_406_NOT_ACCEPTABLE

@app.route('/datos_informe', methods=['GET'])
def get_datos_informe():
	return jsonify(datos_informe())



@app.route('/datos_contratista/<string:identificacion>', methods=['GET'])
def get_datos_contratista(identificacion):
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
	app.run(host='0.0.0.0', debug=True, port=int(parametrosBase["appport"]))
