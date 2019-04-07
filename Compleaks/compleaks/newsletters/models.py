from datetime import datetime
from compleaks import db

class teste():
	
	id = db.Column(db.Integer, primary_key=True)
		

class Divulgacao(teste, db.Model):

	__tablename__ = 'divulgacoes'

	title = db.Column(db.String, unique=True)
	html = db.Column(db.String(50), unique=True)
	body = db.Column(db.Text)
	data_criacao = db.Column(db.DateTime, default=datetime.now)
	last_send = db.Column(db.DateTime, default=None, nullable=True)


	def __init__(self, title, body, html):
		super(teste, self).__init__()
		self.title = title
		self.html = html
		self.body = body

class Material(teste, db.Model):

	__tablename__ = 'materiais'

	title = db.Column(db.String(50), unique=True)
	arquivo = db.Column(db.String(50), unique=True)
	data_criacao = db.Column(db.DateTime, default=datetime.now)


	def __init__(self, title, arquivo):
		super(teste, self).__init__()
		self.title = title
		self.arquivo = arquivo
