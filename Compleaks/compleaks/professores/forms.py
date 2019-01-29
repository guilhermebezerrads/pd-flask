from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField)
from wtforms.validators import DataRequired, Email

class AdicionarProfessorForm(FlaskForm):

    nome = StringField("Nome completo:", validators=[DataRequired()])
    submit = SubmitField("Adicionar")

class BuscarProfessorForm(FlaskForm):

    nome = StringField("Nome do professor:", validators=[DataRequired()])
    submit = SubmitField("Buscar")

class EditarProfessorForm(FlaskForm):

    id = IntegerField("Id do professor:", validators=[DataRequired()])
    novo_nome = StringField("Novo nome completo:", validators=[DataRequired()])
    submit = SubmitField("Editar")

class ExcluirProfessorForm(FlaskForm):

    id = IntegerField("Id do professor:", validators=[DataRequired()])
    submit = SubmitField("Excluir")