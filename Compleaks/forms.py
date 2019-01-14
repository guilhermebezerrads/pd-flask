from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AdicionarDisciplinaForm(FlaskForm):

	nome = StringField("Nome da disciplina:")
	submit = SubmitField("Adicionar")

class EditarDisciplinaForm(FlaskForm):

	id = IntegerField("ID da disciplina a ser editada:")
	nome = StringField("Novo nome:")
	submit = SubmitField("Salvar")