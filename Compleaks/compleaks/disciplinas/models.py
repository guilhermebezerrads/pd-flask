from datetime import datetime
from compleaks import db

class Disciplina(db.Model):

	__tablename__ = 'disciplinas'

	####### Tabela para disciplina
	# id, nome

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String, unique=True)
	data_criacao = db.Column(db.DateTime, default=datetime.now())

	ativado = db.Column(db.Boolean)
	data_deletado = db.Column(db.DateTime, nullable=True)
	id_deletor = db.Column(db.Integer, nullable=True)
	id_criador = db.Column(db.Integer, nullable=True)
	motivo_delete = db.Column(db.String(120), nullable=True)

	arquivos = db.relationship('Arquivo', backref='disciplina', lazy=True)

	def __init__(self, nome, id_criador):
		self.nome = nome
		self.ativado = True
		self.id_criador = id_criador

	def __repr__(self):
		return "ID: {}. Nome: {}".format(self.id, self.nome)
