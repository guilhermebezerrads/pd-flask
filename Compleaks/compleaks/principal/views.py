from flask import render_template, Blueprint
from compleaks import db

principal = Blueprint('principal', __name__)

@principal.route('/')
def index():
    return render_template('index.html')


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404





