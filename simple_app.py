from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from config import Config 
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from request_logger import log_request_info, log_response_info



app= Flask(__name__)
app.config.from_object(Config)

mysql= MySQL(app)
jwt = JWTManager(app) 


# Register the berfore and after trquest handler
@app.before_request
def before_request():
    log_request_info()
    
@app.after_request
def after_request(response):
    return log_response_info(response)


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(tasks_bp, url_prefix='/tasks')

blacklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist
    
    
@app.route('/todo')
def main():
    return '<h1> Welcome to the main page<h1>'


if __name__ == "__main__":
    app.run(debug=True)
    
    




