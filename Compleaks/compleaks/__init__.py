import os
from flask import Flask, render_template, redirect, flash, url_for, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from compleaks.professores.dapartamentos import lista_unidades_academicas

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

############################################################
################## BANCO DE DADOS ##########################
############################################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)

login_manager.login_view = "usuarios.login"

############################################################
################## EMAIL CONFIG ############################
############################################################

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "jinformatica471@gmail.com"
app.config['MAIL_PASSWORD'] = 'ijunior1034'

mail = Mail(app)
dist = [1,2,3,4,5] 

############################################################
################## BLUEPRINTS ##############################
############################################################


from compleaks.principal.views import principal
from compleaks.usuarios.views import usuarios
from compleaks.arquivos.views import arquivos
from compleaks.professores.views import professores
from compleaks.disciplinas.views import disciplinas
from compleaks.questoes.views import questoes
from compleaks.simulados.views import simulados
from compleaks.newsletters.views import newsletters
from compleaks.error_pages.handlers import error_pages

app.register_blueprint(principal)
app.register_blueprint(usuarios,url_prefix='/usuarios')
app.register_blueprint(arquivos,url_prefix='/arquivos')
app.register_blueprint(professores,url_prefix='/professores')
app.register_blueprint(disciplinas,url_prefix='/disciplinas')
app.register_blueprint(questoes,url_prefix='/questoes')
app.register_blueprint(simulados,url_prefix='/simulados')
app.register_blueprint(newsletters,url_prefix='/newsletters')
app.register_blueprint(error_pages)



####################################
############FUNÇÕES#################
####################################
	

@app.template_filter('converte')
def converte(s):
    return Markup(s)

@app.template_filter('unidade_academica')
def unidade_academica(id):
	lista = lista_unidades_academicas()
	return lista[id][1]

@app.template_filter('define_quantidade')
def define_quantidade(quantidade):
	lista = [(str(i), str(i)+" Questões") for i in range(quantidade) if i >= 3 and i <= 15]
	return lista 