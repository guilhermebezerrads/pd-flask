from app import db


####### Tabela para disciplina
# recomendável ter id, nome


####### Tabela para arquivo
# id, nome, data de upload, tipo de arquivo, disciplina, etc


####### Tabela para usuario
# id, username, email, nome, senha, curso, etc



####### Tabela para Posts no Compleaks, tais como 
####### tutoriais, dicas úteis, etc.
class Post(db.Model):

	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String(100))
	conteudo = db.Column(db.Text)
	data = db.Column(db.DateTime)
	usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

	def __init__(self, titulo, conteudo)
		self.titulo = titulos
		self.conteudo = conteudo
