from flask import render_template, Blueprint, url_for, redirect, flash
from compleaks import db
from compleaks.usuarios.forms import (LoginForm, TrocaEmailForm, 
					TrocaSenhaForm, AdicionarUsuarioForm)
from compleaks.usuarios.models import Usuario

usuarios = Blueprint('usuarios', __name__,template_folder='templates/usuarios')

@usuarios.route('/adicionar', methods=['POST', 'GET'])
def adicionar():
	form = AdicionarUsuarioForm()

	if form.validate_on_submit():
		#faz algo
		print("faz algo")

	return render_template('adicionar_usuario.html', form=form)


@usuarios.route('/editar', methods=['POST', 'GET'])
def editar():
	pass

@usuarios.route('/listar', methods=['POST', 'GET'])
def listar():
	pass

@usuarios.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		#é preciso verificar se dados conferem no banco de dados

		flash("Você foi logado com sucesso.")
		return redirect(url_for('index'))

	return render_template('login.html', form=form)


@usuarios.route('/troca-informacao', methods=['POST', 'GET'])
def troca():

    form_email = TrocaEmailForm()
    form_senha =  TrocaSenhaForm()
    return render_template('troca_informacao.html', form_email=form_email, form_senha=form_senha)
