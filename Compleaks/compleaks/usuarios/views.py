from flask import (render_template, request,
					 Blueprint, url_for, redirect, flash, abort)
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_user,login_required,logout_user
from compleaks import db
from compleaks.usuarios.forms import (LoginForm, TrocaEmailForm, 
										TrocaSenhaForm, AdicionarUsuarioForm,
										BuscarUsuarioForm)
from compleaks.usuarios.models import Usuario
from datetime import datetime

usuarios = Blueprint('usuarios', __name__,template_folder='templates/usuarios')

@usuarios.route('/cadastro', methods=['POST', 'GET'])
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

		flash("Obrigado por se juntar, disfrute o máximo possível do Compleaks!")

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
	flash("Usuário deslogado com sucesso!")
	return redirect(url_for('principal.index'))

@usuarios.route('/lista', methods=['POST', 'GET'])
@login_required
def listar():
	if not current_user.is_admin:
		abort(403)

	users = Usuario.query.order_by(Usuario.username)
	return render_template('todos_users.html', users=users)

@usuarios.route('/busca', methods=['POST', 'GET'])
@login_required
def buscar():
	form = BuscarUsuarioForm()
	users = Usuario.query.order_by(Usuario.username.desc())
	existe_user = True

	if form.validate_on_submit():

		if int(form.filtrar.data) == 1:
			
			existe_user = Usuario.query.filter(Usuario.username.contains(form.username.data)).first()
			users = Usuario.query.filter(Usuario.username.contains(form.username.data)).all()
		
		if int(form.filtrar.data) == 2:				
			existe_user = Usuario.query.filter(Usuario.nome.contains(form.nome.data)).first()
			users = Usuario.query.filter(Usuario.nome.contains(form.nome.data)).all()

		if int(form.filtrar.data) is 3:
			existe_user = Usuario.query.filter(Usuario.email.contains(form.email.data)).first()
			admin_only = Usuario.query.filter(Usuario.email.contains(form.email.data)).all()

		admin_only = form.administrators.data

		return render_template('buscar.html',admin_only=admin_only, users=users, existe_user=existe_user, form=form)

	return render_template('buscar.html',admin_only=False, users=users, existe_user=existe_user, form=form)

@usuarios.route('/exclusao/<int:user_id>', methods=['POST', 'GET'])
@login_required
def deletar(user_id):
	if not current_user.is_admin:
		abort(403)

	user = Usuario.query.get_or_404(user_id)

	if current_user == user:
		flash("Você não pode se deletar do sistema")
		abort(403)
	
	user.is_eligible = False
	user.data_deletado = datetime.now()
	user.id_deletor = current_user.id

	if request.method == "POST":
		try:
			user.motivo_delete = request.form.get("motivo{}".format(user_id))
		except Exception as e:
			flash("Aqui não tem bobo não porra!")
			print(e)#pretendo mandar um email avisando que alguem tentou uma violação
			abort(403)
		
	db.session.commit()
	flash("Usuário acabou de se tornar inoperante no sistema!")
	return redirect(url_for('usuarios.listar'))

@usuarios.route('/redefinicao/<int:user_id>', methods=['POST', 'GET'])
@login_required
def redefinir(user_id):
	if not current_user.is_admin:
		abort(403)
	user = Usuario.query.filter_by(id=user_id)
	user.is_eligible = True
	user.data_deletado = None
	user.id_deletor = None

	user.motivo_delete = None
		
	db.session.commit()
	flash("Usuário acabou de redefinido ao sistema!")
	return redirect(url_for('usuarios.listar'))

@usuarios.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = Usuario.query.filter_by(email=form.email.data).first()

		if user.check_password(form.senha.data) and user is not None and user.is_eligible is True:
			
			login_user(user)
			flash("Logado com Sucesso!")
			
			return redirect(url_for('principal.index'))

		elif not user.is_eligible:
			flash("Você foi banido do sistema por: {}".format(user.motivo_delete))


	return render_template('login.html', form=form)


@usuarios.route('/troca', methods=['POST', 'GET'])
@login_required
def troca():
	
	form_email = TrocaEmailForm()
	form_senha =  TrocaSenhaForm()

	if form_email.validate_on_submit():
		if Usuario.query.filter_by(email=form_email.email.data):
			flash(f"O e-mail já está e uso!")
			
		elif current_user.check_password(form_email.senha_atual.data):
			current_user.email = form_email.novo_email.data
			db.session.commit()
			flash("Email trocado com sucesso!")
		
		else:
			flash("Senha atual incorreta!")


	if form_senha.validate_on_submit():
		if current_user.check_password(password=form_senha.senha_atual.data):
			flash(f"A senha atual não é válida!")
		else:
			bcrypt = Bcrypt()
			current_user.hhash = bcrypt.generate_password_hash(form_senha.nova_senha.data)
			db.session.commit()
			flash("Senha trocada com sucesso!")

	

	return render_template('troca_informacao.html',
							form_email=form_email,
							form_senha=form_senha)
