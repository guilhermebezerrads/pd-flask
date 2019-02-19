from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, BooleanField, SelectField)
from wtforms.validators import DataRequired

class AdicionarQuestaoForm(FlaskForm):	
	enunciado = StringField("Enunciado:", validators=[DataRequired()])
	disciplina = SelectField("Disciplina:", validators=[DataRequired()])
	submit = SubmitField("Adicionar")

class AdicionarAlternativaForm(FlaskForm):
	conteudo = StringField("Conteudo:", validators=[DataRequired()])
	correta = BooleanField("Correta:")
	submit = SubmitField("Adicionar")

class EditarQuestaoForm(FlaskForm):
	novo_enunciado = StringField("Enunciado:", validators=[DataRequired()])
	nova_disciplina = SelectField("Disciplina:", validators=[DataRequired()])
	submit = SubmitField("Editar")

class EditarAlternativaForm(FlaskForm):
	novo_conteudo = StringField("Conteudo:", validators=[DataRequired()])
	novo_correta = BooleanField("Correta:")
	submit = SubmitField("Editar")