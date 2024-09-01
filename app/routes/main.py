from flask import Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/todo')
def main():
    return '<h1> Welcome to the main page</h1>'
