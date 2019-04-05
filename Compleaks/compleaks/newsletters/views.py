from flask import (render_template, Blueprint, url_for, redirect,
 					flash, current_app, request, abort, Markup)
from compleaks import db
from flask_login import current_user, login_required
from compleaks.usuarios.models import Usuario
from compleaks.newsletters.models import  Divulgacao
from compleaks.newsletters.forms import LetterForm

newsletters = Blueprint('newsletters', __name__,template_folder='templates/newsletters')

@newsletters.route('/adicionar', methods=['POST', 'GET'])
@login_required
def adicionar():

	if not current_user.is_admin:
		abort(403)

	form = LetterForm()

	if form.validate_on_submit():

		nova = Divulgacao(title=form.titulo.data, body=form.front_end.data)
		db.session.add(nova)
		db.session.commit()
		flash("Newsletters adicionado com sucesso", "success")

	return render_template('novo_letter.html', form=form)


@newsletters.route('/deletar/<int:id>', methods=['POST', 'GET'])
@login_required
def deletar(id):

	if not current_user.is_admin:
		abort(403)

	form = LetterForm()

	delete = Divulgacao.query.get_or_404(id)
	db.session.delete(delete)
	db.session.commit()

	flash("Newsletters adicionado com sucesso", "success")

	return redirect(url_for("newsletters.listar"))


@newsletters.route('/editar/<int:id>', methods=['POST', 'GET'])
@login_required
def editar():

	if not current_user.is_admin:
		abort(403)

	form = LetterForm()
	edit = Divulgacao.query.get_or_404(id)

	if form.validate_on_submit():

		edit.title = form.titulo.data
		edit.body = form.front_end.data
		db.session.commit()
		flash("Newsletters modificado com sucesso", "success")

		return redirect(url_for("newsletters.listar"))

	form.titulo.data = edit.title
	form.front_end.data = edit.body

	return render_template('editar_letter.html', form=form)


@newsletters.route('/listar', methods=['POST', 'GET'])
@login_required
def listar():

	if not current_user.is_admin:
		abort(403)


	page = request.args.get('page', 1, type=int)
	letters = Divulgacao.query.all().order_by(Divulgacao.data_criacao.asc()).paginate(page=page, per_page=10)

	return render_template('lista_letters.html', letters=letters)


def send_email(letter, emails):

	msg = Message(letter.title,
                  sender='noreply@demo.com',
                  recipients=emails)

	msg.html = Markup(letter.body)

	msg.body = "Lembre-se de visitar o Compleaks para ficar em dias com seus estudos. :)"
	mail.send(msg)

def e_mails_disponiveis():

	emails = []

	usuarios = Usuario.query.filter_by(ativado=True)
	for user in usuarios:

		emails.append(user.email)

	return emails


@newsletters.route('/enviar_emails/<int:id>', methods=['POST', 'GET'])
@login_required
def enviar(id):

	if not current_user.is_admin:
		abort(403)

	letter = Divulgacao.query.get_or_404(id)
	emails = e_mails_disponiveis()

	send_email(letter, emails)

	flash("Mensagem envianda com sucesso!", "success")

	return redirect(url_for('newsletters.listar'))