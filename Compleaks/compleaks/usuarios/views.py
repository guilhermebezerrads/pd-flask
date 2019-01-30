from flask import render_template, Blueprint, url_for, redirect, flash
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_user,login_required,logout_user
from compleaks import db
from compleaks.usuarios.forms import (LoginForm, TrocaEmailForm, 
										TrocaSenhaForm, AdicionarUsuarioForm)
from compleaks.usuarios.models import Usuario

usuarios = Blueprint('usuarios', __name__,template_folder='templates/usuarios')

@usuarios.route('/adicionar', methods=['POST', 'GET'])
def adicionar():
	form = AdicionarUsuarioForm()

	if form.validate_on_submit() and not Usuario.query.filter_by(username=form.username.data).first() and not Usuario.query.filter_by(email=form.email.data).first(): 
		bcript = Bcrypt()

		nome = form.nome.data
		username = form.username.data
		email = form.email.data
		hhash = bcript.generate_password_hash(form.senha.data) 
		curso = form.curso.data
		periodo = form.periodo.data
		
		novo_user = Usuario(username, hhash, nome, email, curso, periodo)

		db.session.add(novo_user)
		db.session.commit()

		return redirect(url_for('usuarios.login'))

	if Usuario.query.filter_by(username=form.username.data).first():
		flash(f"O nome de usuário ja existe!")

	if Usuario.query.filter_by(email=form.email.data).first():
		flash(f"O e-mail já está e uso!")

	return render_template('adicionar_usuario.html', form=form)


@usuarios.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('principal.index'))

@usuarios.route('/listar', methods=['POST', 'GET'])
@login_required
def listar():
	if not current_user.is_admin:
		abort(403)

	users = Usuario.query.order_by(Usuario.username.desc())
	return render_template('todos_users.html', users=users)

@usuarios.route('/deletar/<int:user_id>', methods=['POST', 'GET'])
@login_required
def deletar(user_id):
	if not current_user.is_admin:
		abort(403)
	user = Usuario.query.filter_by(id=user_id)
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('usuarios.listar'))

@usuarios.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = Usuario.query.filter_by(email=form.email.data).first()

		if user.check_password(form.senha.data) and user is not None:
			
			login_user(user)
			
			return redirect(url_for('principal.index'))


	return render_template('login.html', form=form)


@usuarios.route('/troca', methods=['POST', 'GET'])
@login_required
def troca():
	
	form_email = TrocaEmailForm()
	form_senha =  TrocaSenhaForm()

	if form_senha.validate_on_submit():
		pass

	if form_email.validate_on_submit():
		if Usuario.query.filter_by(email=form_email.email.data):
			flash(f"O e-mail já está e uso!")
		else:
			current_user.email = form_email.novo_email.data
			db.session.commit()

	if form_senha.validate_on_submit():
		if current_user.check_password(password=form_senha.senha_atual.data):
			flash(f"A senha atual não é válida!")
		else:
			bcrypt = Bcrypt()
			current_user.hhash = bcrypt.generate_password_hash(form_senha.nova_senha.data)
			db.session.commit()
	

	return render_template('troca_informacao.html', form_email=form_email, form_senha=form_senha)
