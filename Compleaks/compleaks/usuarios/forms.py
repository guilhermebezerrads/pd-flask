from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField,
					PasswordField, BooleanField, SelectField)
from wtforms.validators import DataRequired, Email, EqualTo

def prenche_periodos():
	#como em medidica temos até 24 periodos
	periodos = []
	for i in range(24):
		periodos.append((str(i+1), (str(i+1)+'º')))
	return periodos
		

class AdicionarUsuarioForm(FlaskForm):

	username = StringField("Username: ", validators=[DataRequired()])
	nome = StringField("Nome completo: ", validators=[DataRequired()])

	#Transformar, futuramente, os campos de Curso e Periodo em SelectField
	curso = StringField("Curso: ", validators=[DataRequired()])
	periodo = SelectField("Periodo Atual: ", choices=prenche_periodos())
	######################################################################
	
	email = StringField("Email: ", validators=[DataRequired(), Email()])
	senha = PasswordField("Senha: ", validators=[DataRequired(), EqualTo('conf_senha', message="As senhas pressisam de ser igual")])
	conf_senha = PasswordField("Cinfirmar Senha: ", validators=[DataRequired()])

	submit = SubmitField("Adicionar: ")

class LoginForm(FlaskForm):

	email = StringField("Email: ", validators=[DataRequired(), Email()])
	senha = PasswordField("Senha: ", validators=[DataRequired()])
	lembrar = BooleanField("Lembrar-me: ")
	submit = SubmitField("Entrar: ")


class TrocaSenhaForm(FlaskForm):

	senha_atual = PasswordField("Senha atual: ", validators=[DataRequired()])
	nova_senha = PasswordField("Nova senha: ", validators=[DataRequired(), EqualTo('conf_senha', message="As senhas pressisam de ser igual")])
	conf_senha = PasswordField("Confirmar nova senha: ", validators=[DataRequired()])
	submit = SubmitField("Trocar")


class TrocaEmailForm(FlaskForm):

	novo_email = StringField("Novo email", validators=[DataRequired(), Email(), EqualTo('conf_email', message="Os emails pressisam de ser igual")])
	conf_email = StringField("Confirmar email", validators=[DataRequired(), Email()])
	submit = SubmitField("Trocar")
