from compleaks import db, login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin):

	__tablename__ = 'usuarios'

	####### Tabela para usuario
	# id, username, email, nome, senha, curso, etc

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	hhash = db.Column(db.String)
	nome = db.Column(db.String)
	email = db.Column(db.String, unique=True)
	curso = db.Column(db.String)
	periodo = db.Column(db.Integer)
	is_admin = db.Column(db.Integer)

	arquivos = db.relationship('Arquivos', backref='author', lazy=True)

	def __init__(self, username, hhash, nome, email, curso, periodo):
		self.username = username
		self.nome = nome
		self.email = email
		self.hhash = hhash
		self.curso = curso
		self.periodo = periodo
		self.is_admin = 0

	def __repr__(self):
		return """<td scope="row"> {self.id} </td>
				  <td> {self.username} </td>
				  <td> {self.nome} </td>
				  <td> {self.email} </td>
				  <td> {self.curso} </td>
				  <td> {self.periodo} </td>"""
	
	def check_password(self, pasword):
		bcript = Bcrypt()
		return bcript.check_password_hash(self.hhash, pasword)

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