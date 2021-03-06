from compleaks import db, login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin):

	__tablename__ = 'usuarios'

	####### Tabela para usuario
	# id, username, email, nome, senha, curso, etc

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True)
	hhash = db.Column(db.String)
	nome = db.Column(db.String(120))
	email = db.Column(db.String(120), unique=True)
	curso = db.Column(db.String(64))
	periodo = db.Column(db.Integer)
	is_admin = db.Column(db.Integer)
	data_criacao = db.Column(db.DateTime, default=datetime.now)

	avatar = db.Column(db.String(120), default="default_profile.png")
	
	ativado = db.Column(db.Boolean)
	data_deletado = db.Column(db.DateTime, nullable=True)
	id_deletor = db.Column(db.Integer, nullable=True)
	motivo_delete = db.Column(db.String(120), nullable=True)

	arquivos = db.relationship('Arquivo', backref='author', lazy=True)

	avaliacoes = db.relationship('Avaliacao_Arquivo', backref='avaliador', lazy=True)

	simulado = None

	def __init__(self, username, hhash, nome, email, curso, periodo):
		self.username = username
		self.nome = nome
		self.email = email
		self.hhash = hhash
		self.curso = curso
		self.periodo = periodo
		self.is_admin = 0
		self.ativado = True
		self.simulado = None
	
	def check_password(self, pasword):
		bcript = Bcrypt()
		return bcript.check_password_hash(self.hhash, pasword)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return Usuario.query.get(user_id)

'''
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)
	
class Admin(db.Model, UserMixin):

	__tablename__ = 'administradores'

	####### Tabela para usuario
	# id, username, email, nome, senha, curso, etc

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	hhash = db.Column(db.String)
	nome = db.Column(db.String)
	email = db.Column(db.String, unique=True)

	def __init__(self, username, hhash, nome, email, curso, periodo):
		self.username = username
		self.nome = nome
		self.email = email
		self.hhash = hhash

	def __repr__(self):
		return """<td> {self.id} </td>
				  <td> {self.username} </td>
				  <td> {self.nome} </td>
				  <td> {self.email} </td>
				  """

	def check_password(self, hhash):
		bcript = Bcrypt()
        return bcript.check_password_hash(self.hhash, hhash)
'''