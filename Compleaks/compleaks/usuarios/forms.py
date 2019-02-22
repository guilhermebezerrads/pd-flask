from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField,
					PasswordField, BooleanField, SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from compleaks.usuarios.models import Usuario
from flask_wtf.file import FileField, FileAllowed

def prenche_periodos():
	#como em medidica temos até 24 periodos
	periodos = []
	for i in range(24):
		periodos.append((str(i+1), (str(i+1)+'º')))
	return periodos
		
class BuscarUsuarioForm(FlaskForm):
	filtrar = SelectField("Pesquisar por", choices=[('0','Todos'),('1','Username'),
												('2','Nome'), ('3','Email')])
	administrators = BooleanField("Apenas admins")
	username = StringField("Username")
	nome = StringField("Nome completo")
	email = StringField("Email")
	submit = SubmitField("Buscar")

class AdicionarUsuarioForm(FlaskForm):

	username = StringField("Username", validators=[DataRequired(message="Campo Obrigatório"), Length(min=4, max=30, message="Minimo de 4 caracteres e máximo de 30 por favor!")])
	nome = StringField("Nome completo", validators=[DataRequired(message="Campo Obrigatório"), Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])

	#Transformar, futuramente, os campos de Curso e Periodo em SelectField
	curso = StringField("Curso", validators=[DataRequired(message="Campo Obrigatório")])
	periodo = SelectField("Periodo Atual", choices=prenche_periodos(), validators=[DataRequired(message="Campo Obrigatório")])
	######################################################################
	
	email = StringField("Email", validators=[DataRequired(message="Campo Obrigatório"), Email(message="Campo Obrigatório"), Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])
	senha = PasswordField("Senha", validators=[DataRequired(), EqualTo('conf_senha', message="As senhas pressisam de ser igual"), Length(min=0, max=250, message="Minimo de 3 caracteres e máximo de 250 por favor!")])
	conf_senha = PasswordField("Confirmar Senha", validators=[DataRequired(message="Campo Obrigatório")])

	submit = SubmitField("Cadastrar-se")

class LoginForm(FlaskForm):

	email = StringField("Email", validators=[DataRequired(message="Campo Obrigatório"), Email(message="Campo Obrigatório"), Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])
	senha = PasswordField("Senha", validators=[DataRequired(), Length(min=0, max=250, message="Minimo de 3 caracteres e máximo de 250 por favor!")])
	lembrar = BooleanField("Lembrar-me")
	submit = SubmitField("Entrar")


class TrocaSenhaForm(FlaskForm):

	senha_atual = PasswordField("Senha atual", validators=[DataRequired(), Length(min=0, max=250, message="Minimo de 3 caracteres e máximo de 250 por favor!")])
	nova_senha = PasswordField("Nova senha", validators=[DataRequired(), EqualTo('conf_senha', message="As senhas pressisam de ser igual"), Length(min=0, max=250, message="Minimo de 3 caracteres e máximo de 250 por favor!")])
	conf_senha = PasswordField("Confirmar nova senha", validators=[DataRequired(), Length(min=0, max=250, message="Minimo de 3 caracteres e máximo de 250 por favor!")])
	submit = SubmitField("Trocar")


class TrocaEmailForm(FlaskForm):
	
	senha_atual = PasswordField("Senha atual", validators=[DataRequired(), Length(min=0, max=250, message="Minimo de 3 caracteres e máximo de 250 por favor!")])
	novo_email = StringField("Novo email", validators=[DataRequired(), Email(), EqualTo('conf_email', message="Os emails pressisam de ser igual"), Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])
	conf_email = StringField("Confirmar email", validators=[DataRequired(), Email()])
	submit = SubmitField("Trocar")

class RecuperarSenhaFrom(FlaskForm):

	email = StringField("Email Cadastrado: ", validators=[DataRequired(message="Campo Obrigatório"), 
						Email(message="Campo Obrigatório"),
						Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])
	submit = SubmitField("Solicitar")
	
	def check_email_cadastrado(self):
		user = Usuario.query.filter_by(email=self.email.data).first()
		if user:
			return True
		return False

class ResetarSenhaForm(FlaskForm):

	senha = PasswordField("Senha: ", validators=[DataRequired(), EqualTo('conf_senha', message="As senhas pressisam de ser igual"), Length(min=0, max=250, message="Minimo de 3 caracteres e máximo de 250 por favor!")])
	conf_senha = PasswordField("Confirmar Senha: ", validators=[DataRequired(message="Campo Obrigatório")])
	submit = SubmitField('Resetar Senha')

class TrocaAvatarForm(FlaskForm):
	avatar = FileField('Atualizar avatar', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
	submit = SubmitField("Trocar")

class TrocaNomeForm(FlaskForm):
	novo_nome = StringField("Edite seu nome", validators=[DataRequired()])
	submit = SubmitField("Trocar")

class TrocaUsernameForm(FlaskForm):
	novo_username = StringField("Edite seu nome de usuário", validators=[DataRequired()])
	submit = SubmitField("Trocar")

class TrocaCursoForm(FlaskForm):
	novo_curso = StringField("Edite seu curso", validators=[DataRequired()])
	submit = SubmitField("Trocar")

class TrocaPeriodoForm(FlaskForm):
	novo_periodo = SelectField("Edite seu periodo", choices=prenche_periodos(), validators=[DataRequired()])
	submit = SubmitField("Trocar")