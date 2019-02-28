from flask import render_template, Blueprint, url_for, flash
from compleaks import db, mail
from compleaks.usuarios.forms import LoginForm
from compleaks.principal.forms import FeedBackForm
from flask_login import current_user
from flask_mail import Message

principal = Blueprint('principal', __name__)

@principal.route('/')
def index():
	form_login = LoginForm()
	return render_template('index.html', form_login=form_login)

def feedback_mensage(form):
	
	msg = Message(str(form.titulo.data),
                  sender=str(form.email.data),
                  recipients=["jinformatica471@gmail.com"])

	msg.body = f'''Um feedback do tipo: {form.tipo.data}
	Enviado por: {form.email.data}
	Contendo o seguinte conteúdo:
	{form.texto.data}
Se você não solicitou esta modificação, apenas ignore esse email e nenhuma mudança será feita.
'''
	mail.send(msg)


@principal.route('/feedback')
def feedback():
	form_login = LoginForm()
	form = FeedBackForm()

	if form.validate_on_submit():
		feedback_mensage(form)
		flash("Email enviado com sucesso.", "success")

	if current_user.is_authenticated:
		form.email.data = current_user.email

	else:
		form.email.data = ""

	return render_template('feedback.html', form_login=form_login, form=form)

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404





