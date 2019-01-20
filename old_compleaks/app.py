import os
from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AdicionarDisciplinaForm, EditarDisciplinaForm, LoginForm, BuscarMaterialForm, TrocaSenhaForm, TrocaEmailForm, AdicionarConteudoForm, TrocaEmailForm, TrocaSenhaForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():

    form_add = AdicionarConteudoForm()
    return render_template('adicionaConteudo.html', form_add=form_add)

@app.route('/trocaInformacao')
def troca():

    form_email = TrocaEmailForm()
    form_senha =  TrocaSenhaForm()
    return render_template('trocaInformacao.html', form_email=form_email, form_senha=form_senha)

@app.route('/verconsulta')
def verconsulta():
    return render_template('verconsulta.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

###############################################
################### MODELS ####################
###############################################

#from models import Disciplina, Arquivo, Usuario, Post

###############################################
################### VIEWS #####################
###############################################

@app.route('/adicionar-disciplina', methods=['POST', 'GET'])
def adicionar_disciplina():
	form = AdicionarDisciplinaForm()

	if form.validate_on_submit():
		nome = form.nome.data
		nova_disciplina = Disciplina(nome)

		db.session.add(nova_disciplina)
		db.session.commit()

		flash("A disciplina foi adicionada com sucesso.")
		return redirect(url_for('listar_disciplinas'))

	return render_template('adicionar_disciplina.html', form=form)

@app.route('/editar-disciplina', methods=['POST', 'GET'])
def editar_disciplina():
	form = EditarDisciplinaForm()

	if form.validate_on_submit():
		id = form.id.data
		disciplina = Disciplina.query.get(id)
		disciplina.nome = form.nome.data

		db.session.add(disciplina)
		db.session.commit()

		flash("A disciplina foi editada com sucesso.")
		return redirect(url_for('listar_disciplinas'))

	return render_template('editar_disciplina.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		#é preciso verificar se dados conferem no banco de dados

		flash("Você foi logado com sucesso.")
		return redirect(url_for('index'))

	return render_template('login.html', form=form)

@app.route('/buscar', methods=['POST', 'GET'])
def buscar():

	form = BuscarMaterialForm()

	if form.validate_on_submit():

		return redirect(url_for('verconsulta'))

	return render_template('buscar.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
