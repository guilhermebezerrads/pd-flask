from flask import render_template, Blueprint, url_for
from compleaks import db
from compleaks.usuarios.forms import LoginForm

principal = Blueprint('principal', __name__)

@principal.route('/')
def index():
	form = LoginForm()
	return render_template('index.html', form=form)


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404





