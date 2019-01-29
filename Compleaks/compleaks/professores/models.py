from compleaks import db

class Professor(db.Model):

	__tablename__ = 'professores'

	####### Tabela para professor
	# id, nome

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String, unique=True)

	arquivos = db.relationship('Arquivos', backref='professor', lazy=True)

	def __init__(self, nome):
		self.nome = nome

	def __repr__(self):
		return f"ID: {self.id}; Nome: {self.nome}."