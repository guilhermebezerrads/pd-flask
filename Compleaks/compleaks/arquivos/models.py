from compleaks import db
from datetime import datetime
from compleaks.usuarios.models import Usuario
from compleaks.professores.models import Professor
from compleaks.disciplinas.models import Disciplina


class Arquivo(db.Model):

	__tablename__ = 'arquivos'

	id = db.Column(db.Integer, primary_key=True)
	arquivo = db.Column(db.String(120), nullable=False)
	ano = db.Column(db.Integer)
	semestre = db.Column(db.String(80))
	tipo_conteudo = db.Column(db.String(120))
	observacoes = db.Column(db.Text)
	data_submissao = db.Column(db.DateTime, default=datetime.now)
	nota = db.Column(db.Integer, nullable=True)
	
	data_deletado = db.Column(db.DateTime, nullable=True)
	ativado = db.Column(db.Boolean)
	id_deletor = db.Column(db.Integer, nullable=True)
	motivo_delete = db.Column(db.String(600), nullable=True)

	professors = db.relationship(Professor)
	disciplinas = db.relationship(Disciplina)
	usuarios = db.relationship(Usuario)

	professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=True)
	disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'), nullable=False)
	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

	avaliacoes = db.relationship('Avaliacao_Arquivo', backref='arquivo_avaliado', lazy=True)


	def __init__(self, arquivo, disciplina_id, ano, semestre, tipo_conteudo, 
		professor_id, usuario_id, extensao):
		self.arquivo = arquivo
		self.ano = ano
		self.semestre = semestre
		self.tipo_conteudo = tipo_conteudo
		self.disciplina_id = disciplina_id
		self.professor_id = professor_id
		self.usuario_id = usuario_id
		self.ativado = True

class Avaliacao_Arquivo(db.Model):

	__tablename__ = 'avaliacao_arquivo'

	id = db.Column(db.Integer, primary_key=True)
	nota = db.Column(db.Integer, nullable=False)
	data_nota = db.Column(db.DateTime, default=datetime.now)

	arquivos = db.relationship(Arquivo)
	usuarios = db.relationship(Usuario)

	arquivo_id = db.Column(db.Integer, db.ForeignKey('arquivos.id'), nullable=False)
	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

	def __init__(self, nota, usuario_id, arquivo_id):
		self.nota = nota
		self.arquivo_id = arquivo_id
		self.usuario_id = usuario_id


