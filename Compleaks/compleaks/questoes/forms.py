from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, BooleanField, SelectField, TextAreaField)
from wtforms.validators import DataRequired, Length

class AdicionarQuestaoForm(FlaskForm):	

	enunciado = TextAreaField("Enunciado:", validators=[DataRequired(), 
				Length( max=400, message="Máximo de 400 por favor!")])
	disciplina = SelectField("Disciplina:", validators=[DataRequired()])
	correta = SelectField("Correta:", validators=[DataRequired()],
				 choices=[("1","a)"), ("2","b)"), ("3","c)"),("4","d)")])
	opcao_a = StringField("a)", validators=[DataRequired(), 
			Length(min=4, max=120, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	opcao_b = StringField("b)", validators=[DataRequired(),
		Length(min=4, max=120, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	opcao_c = StringField("c)", validators=[DataRequired(),
			Length(min=4, max=120, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	opcao_d = StringField("d)", validators=[DataRequired(),
			Length(min=4, max=120, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
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

