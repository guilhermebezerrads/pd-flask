from datetime import datetime
from compleaks import db

class Disciplina(db.Model):

	__tablename__ = 'disciplinas'

	####### Tabela para disciplina
	# id, nome

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String, unique=True)
	data_criacao = db.Column(db.DateTime, default=datetime.now())
	
	is_eligible = db.Column(db.Boolean)
	data_deletado = db.Column(db.DateTime, nullable=True)
	id_deletor = db.Column(db.Integer, nullable=True)
	motivo_delete = db.Column(db.String(120), nullable=True)

	arquivos = db.relationship('Arquivo', backref='disciplina', lazy=True)

	def __init__(self, nome):
		self.nome = nome
		self.is_eligible = True

	def __repr__(self):
		return f"ID: {self.id} Nome: {self.nome}"