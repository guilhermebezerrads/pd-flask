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
	data_submissao = db.Column(db.DateTime, default=datetime.utcnow)

	professors = db.relationship(Professor)
	disciplinas = db.relationship(Disciplina)
	usuarios = db.relationship(Usuario)

	professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
	disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'), nullable=False)
	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)


	def __init__(self, arquivo, disciplina_id, ano, semestre, tipo_conteudo, 
		professor_id, usuario_id, data):
		self.arquivo = arquivo
		self.ano = ano
		self.semestre = semestre
		self.tipo_conteudo = tipo_conteudo
		self.disciplina_id = disciplina_id
		self.professor_id = professor_id
		self.usuario_id = usuario_id
		self.data_submissao = data

	def __repr__(self):
		
		return "<td> {self.tipo_conteudo} </td>"


def listaDiciplinas():
	todas_disc = Disciplina.query.all()
	lista_form = []
	for diciplin in todas_disc:
		lista_form.append((str(diciplin.id), diciplin.nome))
	return lista_form

def listaProfessores():
	todos_profs = Professor.query.all()
	lista_form = []
	for prof in todos_profs:
		lista_form.append((str(prof.id), prof.nome))
	return lista_form


# class Post(db.Model):

# 	__tablename__ = 'posts'

# 	id = db.Column(db.Integer, primary_key=True)
# 	titulo = db.Column(db.String(100))
# 	conteudo = db.Column(db.Text)
# 	data = db.Column(db.DateTime)
# 	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

# 	def __init__(self, titulo, conteudo):
# 		self.titulo = titulos
# 		self.conteudo = conteudo