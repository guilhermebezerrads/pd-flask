from compleaks import db
from compleaks.disciplinas.models import Disciplina
from compleaks.usuarios.models import Usuario

class Questao(db.Model):

	__tablename__ = 'questoes'

	id = db.Column(db.Integer, primary_key=True)
	enunciado = db.Column(db.Text, nullable=False)
	data_criacao = db.Column(db.DateTime, default=datetime.now)
	correta = db.Column(db.Integer, default=False)

	ativado = db.Column(db.Boolean, default=True)

	disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'), nullable=False)
	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

	alternativas = db.relationship('alternativas', backref='questao', uselist=True)

	def __init__(self, enunciado, disciplina_id, usuario_id, data_criacao, correta):
		self.enunciado = enunciado
		self.disciplina_id = disciplina_id
		self.usuario_id = usuario_id
		self.correta = correta

class Alternativa(object):
	
	__tablename__ = 'alternativas'

	id = db.Column(db.Integer, primary_key=True)
	conteudo = db.Column(db.Text, nullable=False)
	opcao = db.Column(db.Integer)

	questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'), nullable=False)

	def __init__(self, conteudo, questao_id, opcao):
		self.conteudo = conteudo
		self.questao_id = questao_id
		self.opcao = opcao

