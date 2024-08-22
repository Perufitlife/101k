from flask import Flask, Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_session import Session  # Importa Flask-Session
from config import DATABASE_URL, MAIL_DEFAULT_SENDER, MAIL_PASSWORD, MAIL_SERVER, MAIL_USERNAME, SECRET_KEY, MAIL_PORT, MAIL_USE_TLS

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
sess = Session()  # Inicializa Flask-Session

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuración de correo
    app.config.update(
        MAIL_SERVER=MAIL_SERVER,
        MAIL_PORT=MAIL_PORT,
        MAIL_USE_TLS=MAIL_USE_TLS,
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_DEFAULT_SENDER=MAIL_DEFAULT_SENDER,
    )

    # Configuración de la sesión
    app.config['SESSION_TYPE'] = 'filesystem'  # Puedes cambiar a Redis, Memcached, etc.
    app.config['SECRET_KEY'] = SECRET_KEY

    sess.init_app(app)

    mail.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar blueprints
    from app.views.auth.auth import auth as auth_blueprint
    from app.views.dashboard.dashboard import dashboard as dashboard_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(dashboard_blueprint, url_prefix='/')

    return app
