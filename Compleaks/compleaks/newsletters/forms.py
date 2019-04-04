from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Length

class LetterForm(FlaskForm):

	titulo = StringField("Título do e-mail:", validators=[DataRequired(), 
			Length(min=4, max=20, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	fornt_end = TextAreaField("Coloque o html com CSS inline aqui:", validators=[DataRequired()])

	submit = SubmitField("Submit")