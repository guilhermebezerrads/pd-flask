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
	comentarios = db.relationship('ComentarioDisc', backref='disciplina', lazy=True)

	def __init__(self, nome, id_criador):
		self.nome = nome
		self.ativado = True
		self.id_criador = id_criador

	def __repr__(self):
		return "ID: {}. Nome: {}".format(self.id, self.nome)

class ComentarioDisc(db.Model):
	
	__tablename__ = 'comentarios_disc'

	id = db.Column(db.Integer, primary_key=True)
	conteudo = db.Column(db.Text, nullable=False)
	data_criacao = db.Column(db.DateTime, default=datetime.now)

	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
	disciplina_id= db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)

	respondeu_id = db.Column(db.Integer, nullable=False)

	def __init__(self, conteudo, disciplina_id, usuario_id, respondeu_id=0):
		self.conteudo = conteudo
		self.disciplina_id = disciplina_id
		self.usuario_id = usuario_id
		self.respondeu_id = respondeu_id
