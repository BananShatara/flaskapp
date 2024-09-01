from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager


mysql = MySQL()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    mysql.init_app(app)
    jwt.init_app(app)

    from app.utils.logger import log_request_info, log_response_info

    app.before_request(log_request_info)
    app.after_request(log_response_info)

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(main_bp)

    return app
