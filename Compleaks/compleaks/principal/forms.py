from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, TextAreaField)
from wtforms.validators import DataRequired, Length, Email

class FeedBackForm(FlaskForm):	

	texto = TextAreaField("Menssagem:", validators=[DataRequired(), 
				Length( max=1000, message="Máximo de 400 por favor!")])
	tipo = SelectField("Tipo de FeedBack:", validators=[DataRequired()],
				 choices=[("Sugestão de melhoria","Sugestão de melhoria"),
				  ("Reclamações","Reclamações"), ("Repostar Erro","Repostar Erro"),
				  ("Outro","Outro")])
	titulo = StringField("Titulo", validators=[DataRequired(), 
			Length(max=60, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	email = StringField("Seu email para contato", validators=[DataRequired(), Email()])
	
	submit = SubmitField("Enviar FeedBack")
