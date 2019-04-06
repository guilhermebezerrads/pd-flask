from flask import (render_template, Blueprint, url_for, redirect,
 					flash, current_app, request, abort, Markup)
from compleaks import db, mail
from flask_login import current_user, login_required
from flask_mail import Message
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

		target = os.path.join(current_app.root_path, 'newsletters/templates/newsletters/uploads')
		file = form_add.arquivo.data
		filename = file.filename
		destination = "/".join([target, filename])
		file.save(destination)
		os.remove(destination)

		nova = Divulgacao(title=form.titulo.data, body=form.front_end.data, html=filename)
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
def editar(id):

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
	letters = Divulgacao.query.order_by(Divulgacao.data_criacao.asc()).paginate(page=page, per_page=10)

	return render_template('lista_letters.html', letters=letters)


def send_email(letter, user):

	msg = Message(letter.title,
                  sender='jinformatica471@gmail.com',
                  recipients=[user.email])

	msg.html = render_template("uploads/"+letter.html, user=user)
	msg.body = letter.body
	mail.send(msg)


@newsletters.route('/enviar_emails/<int:id>', methods=['POST', 'GET'])
@login_required
def enviar(id):

	if not current_user.is_admin:
		abort(403)

	letter = Divulgacao.query.get_or_404(id)

	usuarios = Usuario.query.filter_by(ativado=True)

	for user in usuarios:

		send_email(letter=letter, user=user)

	flash("Mensagens enviandas!", "info")

	return redirect(url_for('newsletters.listar'))


@newsletters.route('/testar/<int:id>', methods=['POST', 'GET'])
@login_required
def testar(id):

	if not current_user.is_admin:
		abort(403)

	letter = Divulgacao.query.get_or_404(id)

	teste_user = Usuario("Teste User", "hhash", "Teste letters", "email@teste.com", 
							"O sistema aqui é bruto", 12)

	return render_template('uploads/'+letter.html, user=teste_user)