from flask_wtf import FlaskForm
import datetime
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Email

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


class TrocaSenhaForm(FlaskForm):

	senha_atual = StringField("Senha Atual: ", validators=[DataRequired()])
	nova_senha = StringField("Nova Senha: ", validators=[DataRequired()])
	conf_senha = StringField("Confirmar Nova Senha: ", validators=[DataRequired()])
	submit = SubmitField("Trocar")


class TrocaEmailForm(FlaskForm):

	novo_email = StringField("Novo Email ", validators=[DataRequired()], Email())
	conf_email = StringField("Confirmar Email: ", validators=[DataRequired(), Email()])
	submit = SubmitField("Trocar")


class AdicionarConteudoForm(FlaskForm):

	disciplina = SelectField("Diciplina do arquivo:", choices=["Implementar depois"])
	ano = IntegerFiel("Ano de referência do conteúdo:", validators=[DataRequired(), NumberRange( min = 2010 , max = datetime.datetime.now().year + 1) ])
	Semestre = SelectField("Semestre de referência:", choices=[('1','1°'),('2','2°')], validators=[DataRequired()])
	tipo_conteudo = SelectField("Tipo do conteúdo:", choices=[('apostila','Apostila'),('slide','Apresentação/Slides'),('lista','Lista de exercícios'),('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')], validators=[DataRequired()])
	nome_professor = StringField("Nome do Professor: ", validators=[DataRequired()])
	obsevacoes = StringField("Observações: ", validators=[DataRequired()])
	arquivo = FileField("Arquivo ", validators=[DataRequired()])
	submit = SubmitField("Contribuir")
