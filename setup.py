#!/usr/bin/env python

from setuptools import setup

setup(name='servicio_documentacion',
      version='0.1',
      description='Aplicacion para la generacion de documentos relevantes para el proceso de desarrollo',
      url='http://github.com/faparraf/servicio_documentacion',
      author='udistrital',
      author_email='',
      license='MIT',
      install_requires=[
          'flask',
          'Jinja2',
          'jinja2_markdown',
          'requests',
          'iso8601',
          'flask_api',
          'pdfkit',
          'django-wkhtmltopdf',
      ],
      zip_safe=False)
