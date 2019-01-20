from compleaks import db
from datetime import datetime

class Arquivo(db.Model):

	__tablename__ = 'arquivos'

	id = db.Column(db.Integer, primary_key=True)
	arquivo = db.Column(db.String(120), nullable=False)
	ano = db.Column(db.Integer)
	semestre = db.Column(db.String(80))
	tipo_conteudo = db.Column(db.String(120))
	observacoes = db.Column(db.Text)
	data_submissao = db.Column(db.DateTime, default=datetime.utcnow)

	professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
	disciplina_id = db.Column(db.Integer, nullable=False, db.ForeignKey('disciplinas.id'))
	usuario_id = db.Column(db.Integer, nullable=False, db.ForeignKey('usuarios.id'))

	def __init__(self, arquivo, disciplina_id, ano, semestre, tipo_conteudo, 
		professor_id, usuario_id):
		self.arquivo = arquivo
		self.ano = ano
		self.semestre = semestre
		self.tipo_conteudo = tipo_conteudo
		self.disciplina_id = disciplina_id
		self.professor_id = professor_id
		self.usuario_id = usuario_id

class Disciplina(db.Model):

	__tablename__ = 'disciplinas'

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String, unique=True, nullable=False)
    
	def __init__(self, nome):
		self.nome = nome

	def __repr__(self):
		return ""<td> {self.id} </td>
				  <td> {self.nome} </td>""


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