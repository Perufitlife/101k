from decouple import config
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Definición de las variables de configuración
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or "12345"
DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
STRIPE_API_KEY = config('STRIPE_API_KEY')
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.zoho.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
MAIL_DEFAULT_SENDER = MAIL_USERNAME
