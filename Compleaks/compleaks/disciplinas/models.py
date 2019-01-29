from compleaks import db

class Disciplina(db.Model):

	__tablename__ = 'disciplinas'

	####### Tabela para disciplina
	# id, nome

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String, unique=True)

	arquivos = db.relationship('Arquivo', backref='disciplina', lazy=True)

	def __init__(self, nome):
		self.nome = nome

	def __repr__(self):
		return f"ID: {self.id} Nome: {self.nome}"