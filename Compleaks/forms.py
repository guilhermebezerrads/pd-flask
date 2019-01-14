from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired

class AdicionarDisciplinaForm(FlaskForm):

	nome = StringField("Nome da disciplina:")
	submit = SubmitField("Adicionar")

class EditarDisciplinaForm(FlaskForm):

	id = IntegerField("ID da disciplina a ser editada:")
	nome = StringField("Novo nome:")
	submit = SubmitField("Salvar")

class LoginForm(FlaskForm):

	username = StringField("Nome de usuário:", validators=[DataRequired()])
	password = PasswordField("Senha:", validators=[DataRequired()])
	remember_me = BooleanField("Lembrar me:")
	submit = SubmitField("Entrar")

class BuscarMaterialForm(FlaskForm):

	disciplina = StringField("Disciplina:")
	tipo_arquivo = SelectField("Tipo do arquivo:", choices=[('apostila','Apostila'),('slide','Apresentação/Slides'),('lista','Lista de exercícios'),('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')])
	professor = StringField("Professor:")
	submit = SubmitField("Buscar")