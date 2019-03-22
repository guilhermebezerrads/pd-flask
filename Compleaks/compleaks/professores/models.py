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

	ativado = db.Column(db.Boolean)
	data_deletado = db.Column(db.DateTime, nullable=True)
	id_deletor = db.Column(db.Integer, nullable=True)
	id_criador = db.Column(db.Integer, nullable=True)
	motivo_delete = db.Column(db.String(120), nullable=True)

	arquivos = db.relationship('Arquivo', backref='professor', lazy=True)
	comentarios = db.relationship('ComentarioProf', backref='professor', lazy=True)

	def __init__(self, nome, unidade_academica_id, id_criador):
		self.nome = nome
		self.unidade_academica_id = unidade_academica_id
		self.ativado = True
		self.id_criador = id_criador

	def __repr__(self):
		return f"ID: {self.id}; Nome: {self.nome}."

class ComentarioProf(db.Model):
	
	__tablename__ = 'comentarios_prof'

	id = db.Column(db.Integer, primary_key=True)
	conteudo = db.Column(db.Text, nullable=False)
	data_criacao = db.Column(db.DateTime, default=datetime.now)

	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
	professor_id= db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)

	respondeu_id = db.Column(db.Integer, nullable=False)

	def __init__(self, conteudo, professor_id, usuario_id, respondeu_id=0):
		self.conteudo = conteudo
		self.professor_id = professor_id
		self.usuario_id = usuario_id
		self.respondeu_id = respondeu_id
