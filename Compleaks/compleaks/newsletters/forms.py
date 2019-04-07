from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField, IntegerField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Length

class LetterForm(FlaskForm):

	titulo = StringField("Título do e-mail:", validators=[DataRequired(), 
			Length(min=4, max=20, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	html = FileField("Arquivo html:", validators=[FileRequired(), FileAllowed(['html'])])
	front_end = TextAreaField("Coloque uma body para e-mails que não suportam html")

	submit = SubmitField("Submit")

images = UploadSet('images', IMAGES)

class MaterialForm(FlaskForm):

	titulo = StringField("Título do e-mail:", validators=[DataRequired(), 
			Length(min=4, max=20, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	arquivo = FileField("Arquivo html:", validators=[FileRequired(), FileAllowed(images, 'Apenas imagens')])

	submit = SubmitField("Submit")