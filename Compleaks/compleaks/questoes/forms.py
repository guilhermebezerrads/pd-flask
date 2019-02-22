from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, BooleanField, SelectField, TextField)
from wtforms.validators import DataRequired

class AdicionarQuestaoForm(FlaskForm):	
	enunciado = TextField("Enunciado:", validators=[DataRequired()])
	disciplina = SelectField("Disciplina:", validators=[DataRequired()])
	correta = SelectField("Correta:", validators=[DataRequired()],
				 choices=[(1,"a"), (2,"b"), (3,"c"),(4,"d")])
	opcao_a = StringField("a)", validators=[DataRequired()])
	opcao_b = StringField("b)", validators=[DataRequired()])
	opcao_c = StringField("c)", validators=[DataRequired()])
	opcao_d = StringField("d)", validators=[DataRequired()])
	submit = SubmitField("Adicionar")
	

class EditarQuestaoForm(FlaskForm):
	enunciado = StringField("Enunciado:", validators=[DataRequired()])
	disciplina = SelectField("Disciplina:", validators=[DataRequired()])
	correta = SelectField("Correta:", validators=[DataRequired()],
				 choices=[(1,"a"), (2,"b"), (3,"c"),(4,"d")])
	opcao_a = StringField("a)", validators=[DataRequired()])
	opcao_b = StringField("b)", validators=[DataRequired()])
	opcao_c = StringField("c)", validators=[DataRequired()])
	opcao_d = StringField("d)", validators=[DataRequired()])
	submit = SubmitField("Adicionar")

