# run.py
import os
from dotenv import load_dotenv
from flask import session
from app import create_app, db
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
migrate = Migrate(app, db)

# Función para depurar el contenido de la sesión en cada solicitud
@app.before_request
def before_request():
    print(f"Contenido de la sesión al inicio de la solicitud: {session}")

if __name__ == "__main__":
    app.run(host='localhost', port=8000, debug=os.getenv('FLASK_ENV') != 'production')
