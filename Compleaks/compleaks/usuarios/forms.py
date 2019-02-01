from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField,
					PasswordField, BooleanField, SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

def prenche_periodos():
	#como em medidica temos até 24 periodos
	periodos = []
	for i in range(24):
		periodos.append((str(i+1), (str(i+1)+'º')))
	return periodos
		

class AdicionarUsuarioForm(FlaskForm):

	username = StringField("Username: ", validators=[DataRequired(message="Campo Obrigatório"), Length(min=4, max=30, message="Minimo de 4 caracteres e máximo de 30 por favor!")])
	nome = StringField("Nome completo: ", validators=[DataRequired(message="Campo Obrigatório"), Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])

	#Transformar, futuramente, os campos de Curso e Periodo em SelectField
	curso = StringField("Curso: ", validators=[DataRequired(message="Campo Obrigatório")])
	periodo = SelectField("Periodo Atual: ", choices=prenche_periodos(), validators=[DataRequired(message="Campo Obrigatório")])
	######################################################################
	
	email = StringField("Email: ", validators=[DataRequired(message="Campo Obrigatório"), Email(message="Campo Obrigatório"), Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])
	senha = PasswordField("Senha: ", validators=[DataRequired(), EqualTo('conf_senha', message="As senhas pressisam de ser igual"), Length(min=6, max=30, message="Minimo de 6 caracteres e máximo de 30 por favor!")])
	conf_senha = PasswordField("Cinfirmar Senha: ", validators=[DataRequired(message="Campo Obrigatório"), Length(min=6, max=30, message="Minimo de 6 caracteres e máximo de 30 por favor!")])

	submit = SubmitField("Adicionar: ")

class LoginForm(FlaskForm):

	email = StringField("Email: ", validators=[DataRequired(message="Campo Obrigatório"), Email(message="Campo Obrigatório"), Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])
	senha = PasswordField("Senha: ", validators=[DataRequired(), Length(min=6, max=30, message="Minimo de 6 caracteres e máximo de 30 por favor!")])
	submit = SubmitField("Entrar: ")


class TrocaSenhaForm(FlaskForm):

	senha_atual = PasswordField("Senha atual: ", validators=[DataRequired(), Length(min=6, max=30, message="Minimo de 6 caracteres e máximo de 30 por favor!")])
	nova_senha = PasswordField("Nova senha: ", validators=[DataRequired(), EqualTo('conf_senha', message="As senhas pressisam de ser igual"), Length(min=6, max=30, message="Minimo de 6 caracteres e máximo de 30 por favor!")])
	conf_senha = PasswordField("Confirmar nova senha: ", validators=[DataRequired(), Length(min=6, max=30, message="Minimo de 6 caracteres e máximo de 30 por favor!")])
	submit = SubmitField("Trocar")


class TrocaEmailForm(FlaskForm):
	
	senha_atual = PasswordField("Senha atual: ", validators=[DataRequired(), Length(min=6, max=30, message="Minimo de 6 caracteres e máximo de 30 por favor!")])
	novo_email = StringField("Novo email", validators=[DataRequired(), Email(), EqualTo('conf_email', message="Os emails pressisam de ser igual"), Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])
	conf_email = StringField("Confirmar email", validators=[DataRequired(), Email(), Length(min=3, max=120, message="Minimo de 3 caracteres e máximo de 120 por favor!")])
	submit = SubmitField("Trocar")
