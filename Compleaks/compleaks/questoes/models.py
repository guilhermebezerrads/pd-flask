from compleaks import db
from compleaks.disciplinas.models import Disciplina
from compleaks.usuarios.models import Usuario
from datetime import datetime

class Questao(db.Model):

	__tablename__ = 'questoes'

	id = db.Column(db.Integer, primary_key=True)
	enunciado = db.Column(db.Text, nullable=False)
	data_criacao = db.Column(db.DateTime, default=datetime.now)
	correta = db.Column(db.Integer, default=False)

	ativado = db.Column(db.Boolean, default=True)

	disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'), nullable=False)
	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
	materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'))

	alternativas = db.relationship('Alternativa', backref='questao', uselist=True)

	def __init__(self, enunciado, disciplina_id, usuario_id, correta, materia_id):
		self.enunciado = enunciado
		self.disciplina_id = disciplina_id
		self.usuario_id = usuario_id
		self.correta = correta
		self.materia_id = materia_id

class Alternativa(db.Model):
	
	__tablename__ = 'alternativas'

	id = db.Column(db.Integer, primary_key=True)
	conteudo = db.Column(db.Text, nullable=False)
	opcao = db.Column(db.Integer)

	questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'), nullable=False)

	def __init__(self, conteudo, questao_id, opcao):
		self.conteudo = conteudo
		self.questao_id = questao_id
		self.opcao = opcao

class Comentario(db.Model):
	
	__tablename__ = 'comentarios'

	id = db.Column(db.Integer, primary_key=True)
	conteudo = db.Column(db.Text, nullable=False)
	data_criacao = db.Column(db.DateTime, default=datetime.now)

	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
	questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'), nullable=False)

	respondeu_id = db.Column(db.Integer, nullable=False)

	def __init__(self, conteudo, questao_id, usuario_id, respondeu_id):
		self.conteudo = conteudo
		self.questao_id = questao_id
		self.usuario_id = usuario_id
		self.respondeu_id = respondeu_id