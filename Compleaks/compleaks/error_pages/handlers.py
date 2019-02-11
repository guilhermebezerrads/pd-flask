from flask import Blueprint,render_template
from compleaks.usuarios.forms import LoginForm

error_pages = Blueprint('error_pages',__name__)

@error_pages.app_errorhandler(404)
def error_404(error):
	form_login = LoginForm()
	return render_template('error_pages/404.html', form_login=form_login) , 404

@error_pages.app_errorhandler(403)
def error_403(error):
	form_login = LoginForm()
	return render_template('error_pages/403.html', form_login=form_login) , 403
