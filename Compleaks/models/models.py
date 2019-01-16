from Compleaks import db


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


class Usuario(db.Model):

	__tablename__ = 'usuarios'

	####### Tabela para usuario
	# id, username, email, nome, senha, curso, etc

	id = db.Collumn(db.Integer, primary_key=True, auto_increment=True)
	username = db.Collumn(db.String, unique=True)
	pasword = db.Collumn(db.String)
    nome = db.Collumn(db.String)
    email = db.Collumn(db.String, unique=True)
	curso = db.Collumn(db.String)
	periodo = db.Collumn(db.Integer)

	def __init__(self, id, username, pasword, nome, email, curso):
		self.id = id
		self.username = username
		self.name = name
		self.email = email
		self.pasword = pasword
		self.curso = curso

	def __repr__(self):
		return """<td> {self.id} </td>
				  <td> {self.username} </td>
				  <td> {self.nome} </td>
				  <td> {self.email} </td>
				  <td> {self.curso} </td>
				  <td> {self.periodo} </td>"""
