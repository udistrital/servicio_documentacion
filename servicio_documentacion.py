from flask import Flask
from controllers import documento_pago
app = Flask(__name__)


@app.route('/documento_mensual')
def hello():
    return generar_documento_pago(None)

if __name__ == '__main__':
    app.run()
