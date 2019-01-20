from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField,
	PasswordField, BooleanField)
from wtforms.validators import DataRequired, Email


class AdicionarUsuarioForm(FlaskForm):

	username = StringField("Username", validators=[DataRequired()])
	nome = StringField("Nome completo", validators=[DataRequired()])

	#Transformar, futuramente, os campos de Curso e Periodo em SelectField
	curso = StringField("Curso", validators=[DataRequired()])
	periodo = StringField("Período atual", validators=[DataRequired()])
	######################################################################
	
	email = StringField("Email", validators=[DataRequired(), Email()])
	senha = PasswordField("Senha", validators=[DataRequired()])

	submit = SubmitField("Adicionar")

class LoginForm(FlaskForm):

	username = StringField("Username", validators=[DataRequired()])
	senha = PasswordField("Senha", validators=[DataRequired()])
	lembrar = BooleanField("Lembrar-me")
	submit = SubmitField("Entrar")


class TrocaSenhaForm(FlaskForm):

	senha_atual = PasswordField("Senha atual", validators=[DataRequired()])
	nova_senha = PasswordField("Nova senha", validators=[DataRequired()])
	conf_senha = PasswordField("Confirmar nova senha", validators=[DataRequired()])
	submit = SubmitField("Trocar")


class TrocaEmailForm(FlaskForm):

	novo_email = StringField("Novo email", validators=[DataRequired(), Email()])
	conf_email = StringField("Confirmar email", validators=[DataRequired(), Email()])
	submit = SubmitField("Trocar")
