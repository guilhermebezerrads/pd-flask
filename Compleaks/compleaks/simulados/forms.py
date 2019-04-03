from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField,
                     SubmitField, SelectField, TextAreaField)
from wtforms.validators import DataRequired, Email


class CriarSimuladoForm(FlaskForm):

	disciplina = SelectField("Disciplina:", validators=[DataRequired()])
	submit = SubmitField("Gerar Simulado")

