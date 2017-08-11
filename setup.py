#!/usr/bin/env python

from distutils.core import setup

setup(name='servicio_documentacion',
      version='0.1',
      description='Aplicación para la generación de documentos relevantes para el proceso de desarrollo',
      url='http://github.com/faparraf/servicio_documentacion',
      author='udistrital',
      author_email='',
      license='MIT',
      install_requires=[
          'flask',
          'Jinja2',
          'jinja2_markdown',
      ],
      zip_safe=False)