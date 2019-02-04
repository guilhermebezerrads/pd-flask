from compleaks import db
from datetime import datetime


class Professor(db.Model):

	__tablename__ = 'professores'

	####### Tabela para professor
	# id, nome

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String, unique=True)
	unidade_academica_id = db.Column(db.Integer)
	data_criacao = db.Column(db.DateTime, default=datetime.now())
	
	is_eligible = db.Column(db.Boolean)
	data_deletado = db.Column(db.DateTime, nullable=True)
	id_deletor = db.Column(db.Integer, nullable=True)
	motivo_delete = db.Column(db.String(120), nullable=True)

	arquivos = db.relationship('Arquivo', backref='professor', lazy=True)

	def __init__(self, nome, unidade_academica_id):
		self.nome = nome
		self.is_eligible = True

	def __repr__(self):
		return f"ID: {self.id}; Nome: {self.nome}."