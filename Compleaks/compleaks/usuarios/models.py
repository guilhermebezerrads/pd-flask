from compleaks import db


class Usuario(db.Model):

	__tablename__ = 'usuarios'

	####### Tabela para usuario
	# id, username, email, nome, senha, curso, etc

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	senha = db.Column(db.String)
	nome = db.Column(db.String)
	email = db.Column(db.String, unique=True)
	curso = db.Column(db.String)
	periodo = db.Column(db.Integer)

	def __init__(self, username, senha, nome, email, curso):
		self.username = username
		self.nome = nome
		self.email = email
		self.senha = senha
		self.curso = curso

	def __repr__(self):
		return """<td> {self.id} </td>
				  <td> {self.username} </td>
				  <td> {self.nome} </td>
				  <td> {self.email} </td>
				  <td> {self.curso} </td>
				  <td> {self.periodo} </td>"""
