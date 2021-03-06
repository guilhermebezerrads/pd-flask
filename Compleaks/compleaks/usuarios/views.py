from flask import (render_template, request,
					 Blueprint, url_for, redirect, request, flash, abort)
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_user,login_required,logout_user
from compleaks import db, mail, dist
from compleaks.usuarios.forms import (LoginForm, TrocaEmailForm, 
										TrocaSenhaForm, AdicionarUsuarioForm,
										BuscarUsuarioForm, RecuperarSenhaFrom,
										ResetarSenhaForm, TrocaNomeForm,
										TrocaUsernameForm, TrocaCursoForm,
										TrocaPeriodoForm, TrocaAvatarForm)
from compleaks.usuarios.models import Usuario
from compleaks.arquivos.models import Arquivo
from compleaks.usuarios.avatar_gerenciador import adicionar_avatar
from flask_mail import Message
from datetime import datetime

usuarios = Blueprint('usuarios', __name__,template_folder='templates/usuarios')


@usuarios.route('/perfil/<int:user_id>', methods= ['POST', 'GET'])
def perfil(user_id):

	form_login = LoginForm()

	user = Usuario.query.get_or_404(user_id)
	avatar = url_for('static', filename='images/avatares/'+user.avatar)

	if not user.ativado and current_user.is_authenticated:
		if not user.is_admin:
			abort(404)
	# elif user == current_user:
	# 	return redirect(url_for('usuarios.troca'))

	quantidade = len([arquiv for arquiv in user.arquivos if arquiv.ativado])

	page = request.args.get('page', 1, type=int)	
	arquivos = Arquivo.query\
					.filter(Arquivo.usuario_id\
					.contains(int(user.id)))\
					.filter_by(ativado=True)\
					.paginate(page=page, per_page=12)

	arquivos_row_1 = []
	arquivos_row_2 = []
	arquivos_row_3 = []
	contador = 0
	for arquivo in arquivos.items:
		if contador >= 4:
			break 
		arquivos_row_1.append(arquivo)
		contador = contador + 1

	contador = 0
	for arquivo in arquivos.items:
		if contador >= 8:
			break
		if contador >= 4:
			arquivos_row_2.append(arquivo)
		contador = contador + 1				

	contador = 0
	for arquivo in arquivos.items:
		if contador >= 12:
			break
		if contador >= 8:
			arquivos_row_3.append(arquivo)
		contador = contador + 1				

	arquivos_rows = [arquivos_row_1, arquivos_row_2, arquivos_row_3]

	for row in arquivos_rows:
		for arquivo in row:
			arquivo.avaliado = False

	if current_user.is_authenticated:
		for row in arquivos_rows:
			for arquivo in row:
				for avl in arquivo.avaliacoes:
					if avl in current_user.avaliacoes:
						arquivo.avaliado = True

	total = 0.0
	for row in arquivos_rows:
		for arquivo in row:
			total = 0.0
			if len(arquivo.avaliacoes): 
				for avl in arquivo.avaliacoes:
					total = total + avl.nota
				total = total/len(arquivo.avaliacoes)
			else:
				total = 0.0

			arquivo.nota_decimal = round(total, 1)


	return render_template('usuario_contribuicao.html', user=user, 
							contribuiu=quantidade, arquivos=arquivos, dist=dist,
							form_login=form_login, arquivos_rows=arquivos_rows, 
							avatar=avatar)


def send_wellcome_email(user):

	msg = Message('bem vindo ao compleaks',
                  sender='noreply@demo.com',
                  recipients=[user.email])

	msg.html = render_template("bem_vindo_menssage.html", user=user,
					 link=url_for('usuarios.login', _external=True),
					 link_image=url_for('static', filename='images/Escolar.jpg', _external=True))

	msg.body = f''' Seja muito bem vindo ao Compleaks {user.username}
	Nós realmente estamos animados para facilitar sua vida enquanto estudante. Use e abuse de todo material que conseguir encontrar. Mas sempre lembrando que a sua contribuição para a nossa comunidade faz toda a diferença!

'''
	mail.send(msg)

@usuarios.route('/cadastro', methods=['POST', 'GET'])
def adicionar():

	form_login = LoginForm()

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

		flash("Agradecemos o seu cadastro. Entre agora mesmo na sua conta e aproveite o Compleaks.", "success")
		send_wellcome_email(novo_user)

		return redirect(url_for('usuarios.login'))

	if Usuario.query.filter_by(username=form.username.data).first():
		flash(f"Esse nome de usuário já existe.", "warning")

	if Usuario.query.filter_by(email=form.email.data).first():
		flash(f"Esse e-mail já está em uso.", "warning")

	return render_template('adicionar_usuario.html', form=form, form_login=form_login)


@usuarios.route('/logout')
@login_required
def logout():
	logout_user()
	flash("Você foi deslogado com sucesso.", "success")
	return redirect(url_for('principal.index'))

@usuarios.route('/lista', methods=['POST', 'GET'])
@login_required
def listar():
	if not current_user.is_admin:
		abort(403)

	page = request.args.get('page', 1, type=int)
	users = Usuario.query\
			.order_by(Usuario.username)\
			.paginate(page=page, per_page=10)
	return render_template('todos_users.html', users=users)

@usuarios.route('/busca/<int:admin>/<int:filtro>/<pesquisa>', methods=['POST', 'GET'])
@usuarios.route('/busca',defaults={"filtro":None,"admin":None,"pesquisa":None}, methods=['POST', 'GET'])
@login_required
def buscar(admin,filtro,pesquisa):

	if not current_user.is_admin:
		abort(403)

	form = BuscarUsuarioForm()
	page = request.args.get('page', 1, type=int)
	users = Usuario.query.order_by(Usuario.username).paginate(page=page, per_page=10)
	print(len(users.items))
	existe_user = True
	navigation_data = []
	navigation_data.append(filtro)
	navigation_data.append(admin)
	navigation_data.append(pesquisa)

	if form.validate_on_submit():

		if int(form.filtrar.data) == 1:
			
			pesquisa = form.username.data
			existe_user = Usuario.query.filter(Usuario.username.contains(pesquisa)).first()
			users = Usuario.query\
				.filter(Usuario.username.contains(pesquisa))\
				.paginate(page=page, per_page=10)
		
		if int(form.filtrar.data) == 2:				

			pesquisa = form.nome.data
			existe_user = Usuario.query.filter(Usuario.nome.contains(pesquisa)).first()
			users = Usuario.query.filter(Usuario.nome.contains(pesquisa))\
					.paginate(page=page, per_page=10)

		if int(form.filtrar.data) is 3:

			pesquisa = form.email.data
			existe_user = Usuario.query.filter(Usuario.email.contains(pesquisa)).first()
			users = Usuario.query.filter(Usuario.email.contains(pesquisa))\
					.paginate(page=page, per_page=10)

		admin_only = form.administrators.data

		navigation_data.clear()
		navigation_data.append(int(form.filtrar.data))
		if admin_only:
			navigation_data.append(1)
		else:
			navigation_data.append(0)
		navigation_data.append(pesquisa)

		return render_template('buscar_user.html',admin_only=admin_only, users=users, existe_user=existe_user, navigation_data=navigation_data, form=form)

	if filtro:

		if filtro == 1:
			
			existe_user = Usuario.query.filter(Usuario.username.contains(pesquisa)).first()
			users = Usuario.query\
				.filter(Usuario.username.contains(pesquisa))\
				.paginate(page=page, per_page=10)
		
		if filtro == 2:				
			existe_user = Usuario.query.filter(Usuario.nome.contains(pesquisa)).first()
			users = Usuario.query.filter(Usuario.nome.contains(pesquisa))\
				.paginate(page=page, per_page=10)

		if filtro is 3:
			existe_user = Usuario.query.filter(Usuario.email.contains(pesquisa)).first()
			users = Usuario.query.filter(Usuario.email.contains(pesquisa))\
					.paginate(page=page, per_page=10)

		admin_only = bool(admin)

		return render_template('buscar_user.html',admin_only=admin_only, users=users, existe_user=existe_user, navigation_data=navigation_data, form=form)

	return render_template('buscar_user.html',admin_only=False, users=users, existe_user=existe_user, navigation_data=navigation_data, form=form)

@usuarios.route('/exclusao/<int:user_id>', methods=['POST', 'GET'])
@login_required
def deletar(user_id):
	if not current_user.is_admin:
		abort(403)

	user = Usuario.query.get_or_404(user_id)

	if current_user == user:
		flash("Você não pode desativar a si mesmo do sistema.", "danger")
		abort(403)
	
	user.ativado = False
	user.data_deletado = datetime.now()
	user.id_deletor = current_user.id

	if request.method == "POST":
		try:
			user.motivo_delete = request.form.get("motivo{}".format(user_id))
		except Exception as e:
			flash("Aqui não tem bobo não porra!", "danger")
			abort(403)
		
	db.session.commit()
	flash("O usuário foi desativado do sistema.", "success")
	return redirect(url_for('usuarios.listar'))

@usuarios.route('/redefinicao/<int:user_id>', methods=['POST', 'GET'])
@login_required
def redefinir(user_id):
	if not current_user.is_admin:
		abort(403)
	user = Usuario.query.filter_by(id=user_id)
	user.ativado = True
	user.data_deletado = None
	user.id_deletor = None

	user.motivo_delete = None
		
	db.session.commit()
	flash("O usuário foi ativado novamente no sistema.", "success")
	return redirect(url_for('usuarios.listar'))

@usuarios.route('/login', methods=['POST', 'GET'])
def login():
	form_login = LoginForm()

	if form_login.validate_on_submit():
		user = Usuario.query.filter_by(email=form_login.email.data).first()
		#print(user)

		if user is not None and user.ativado is True:
			
			if user.check_password(form_login.senha.data):

				login_user(user, remember=form_login.lembrar.data)
				flash("Você foi logado com sucesso.", "success")
			
				return redirect(url_for('principal.index'))

			else:
				flash("Email e/ou senha incorretos", "alert")

		if user is not None and not user.ativado:
			flash("Você foi banido do sistema por: {}".format(user.motivo_delete), "warning")

		if user == None:
			flash("Email e/ou senha incorretos", "warning")


	return redirect(url_for('principal.index'))

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Requisição de Troca de Senha Compleaks',
                  sender='noreply@demo.com',
                  recipients=[user.email])

	msg.html = render_template("resetar_senha_menssage.html", link=url_for('usuarios.reset_token', token=token, _external=True))

	msg.body = f'''Para resetar sua senha, segue o link abixo:
{url_for('usuarios.reset_token', token=token, _external=True)}

Se você não solicitou esta modificação, apenas ignore esse email e nenhuma mudança será feita.
'''
	mail.send(msg)


@usuarios.route("/resetar_senha", methods=['GET', 'POST'])
def reset_request():

	form_login = LoginForm()

	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RecuperarSenhaFrom()
	
	if not form.check_email_cadastrado() and form.validate_on_submit():
		flash('Esse email não está cadastrado no sistema', 'dangerus')

	if form.validate_on_submit() and form.check_email_cadastrado():
		
		user = Usuario.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('Um e-mail foi enviado para resetar sua senha! Siga suas devidas instruções.', 'info')
		return redirect(url_for('usuarios.login'))	

	return render_template('forgot_password.html', form=form, form_login=form_login)


@usuarios.route("/resetar_senha/<token>", methods=['GET', 'POST'])
def reset_token(token):

	form_login = LoginForm()

	bcrypt = Bcrypt()
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = Usuario.verify_reset_token(token)

	if user is None:
		flash('Esse token de ativação é invalido ou expirou', 'warning')
		return redirect(url_for('usuarios.reset_request'))
	form = ResetarSenhaForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.senha.data)
		user.senha = hashed_password
		db.session.commit()
		flash('Sua senha foi trocada co sucesso! Já pode se logar no sistema', 'success')
		return redirect(url_for('usuarios.login'))
	
	return render_template('resetar_senha.html', form=form, form_login=form_login)


@usuarios.route('/meu-perfil', methods=['POST', 'GET'])
@login_required
def meu_perfil():
	
	avatar = url_for('static', filename='images/avatares/'+current_user.avatar)

	form_avatar = TrocaAvatarForm()
	form_email = TrocaEmailForm()
	form_senha =  TrocaSenhaForm()
	form_nome = TrocaNomeForm()
	form_username = TrocaUsernameForm()
	form_curso = TrocaCursoForm()
	form_periodo = TrocaPeriodoForm()

	if form_avatar.validate_on_submit():
		username = current_user.username
		if not form_avatar.avatar.data == None:
			pic = adicionar_avatar(form_avatar.avatar.data, username)
			current_user.avatar = pic
			db.session.commit()
			flash("Avatar atualizado com sucesso!", "warning")

	if form_nome.validate_on_submit():
		current_user.nome = form_nome.novo_nome.data
		db.session.commit()
		flash("Nome trocado com sucesso!", "warning")

	if form_username.validate_on_submit():
		current_user.username = form_username.novo_username.data
		db.session.commit()
		flash("Nome de usuário trocado com sucesso!", "warning")
	
	if form_curso.validate_on_submit():
		current_user.curso = form_curso.novo_curso.data
		db.session.commit()
		flash("Curso trocado com sucesso!", "warning")

	if form_periodo.validate_on_submit():
		current_user.periodo = form_periodo.novo_periodo.data
		db.session.commit()
		flash("Periodo trocado com sucesso!", "warning")

	if form_email.validate_on_submit():
		if Usuario.query.filter_by(email=form_email.novo_email.data).first() and not current_user.email == form_email.novo_email.data:
			flash(f"O e-mail já está e uso!", "warning")
			
		elif current_user.check_password(form_email.senha_atual.data) and not current_user.email == form_email.novo_email.data:
			current_user.email = form_email.novo_email.data
			db.session.commit()
			flash("Email trocado com sucesso!", "warning")
		
		elif current_user.email == form_email.novo_email.data:
			flash("O novo email e o antigo não podem ser iguais!", "warning")

		else:
			flash("Senha atual incorreta!", "warning")


	bcrypt = Bcrypt()
	if form_senha.validate_on_submit():
		if current_user.check_password(password=form_senha.senha_atual.data):
			flash(f"A senha atual não é válida!", "warning")
		elif current_user.hhash ==  bcrypt.generate_password_hash(form_senha.nova_senha.data):
			flash("A nova senha e a antiga não podem ser iguais!")
		
		else:
			current_user.hhash = bcrypt.generate_password_hash(form_senha.nova_senha.data)
			db.session.commit()
			flash("Senha trocada com sucesso!", "success")
	
	page = request.args.get('page', 1, type=int)	
	arquivos = Arquivo.query\
					.filter(Arquivo.usuario_id\
					.contains(int(current_user.id)))\
					.filter_by(ativado=True)\
					.paginate(page=page, per_page=12)

	arquivos_row_1 = []
	arquivos_row_2 = []
	arquivos_row_3 = []

	contador = 0
	for arquivo in arquivos.items:
		if contador >= 4:
			break 
		arquivos_row_1.append(arquivo)
		contador = contador + 1

	contador = 0
	for arquivo in arquivos.items:
		if contador >= 8:
			break
		if contador >= 4:
			arquivos_row_2.append(arquivo)
		contador = contador + 1				

	contador = 0
	for arquivo in arquivos.items:
		if contador >= 12:
			break
		if contador >= 8:
			arquivos_row_3.append(arquivo)
		contador = contador + 1					

	arquivos_rows = [arquivos_row_1, arquivos_row_2, arquivos_row_3]

	quantidade = len(arquivos_row_1) + len(arquivos_row_2) + len(arquivos_row_3) 

	for row in arquivos_rows:
		for arquivo in row:
			arquivo.avaliado = False

	if current_user.is_authenticated:
		for row in arquivos_rows:
			for arquivo in row:
				for avl in arquivo.avaliacoes:
					if avl in current_user.avaliacoes:
						arquivo.avaliado = True

	total = 0.0
	for row in arquivos_rows:
		for arquivo in row:
			total = 0.0
			if len(arquivo.avaliacoes): 
				for avl in arquivo.avaliacoes:
					total = total + avl.nota
				total = total/len(arquivo.avaliacoes)
			else:
				total = 0.0

			arquivo.nota_decimal = round(total, 1)



	return render_template('perfil_usuario.html',
							form_email=form_email,
							form_senha=form_senha,
							arquivos_rows=arquivos_rows,
							contribuiu=quantidade, 
							dist=dist,
							arquivos=arquivos, 
							current_user=current_user,
							form_nome=form_nome,
							form_username=form_username,
							form_curso=form_curso,
							form_periodo=form_periodo,
							form_avatar=form_avatar,
							avatar=avatar)