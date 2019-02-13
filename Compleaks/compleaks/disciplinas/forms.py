from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField)
from wtforms.validators import DataRequired, Length

class AdicionarDisciplinaForm(FlaskForm):

    nome = StringField("Nome da disciplina:", validators=[DataRequired()])
    submit = SubmitField("Adicionar")

class BuscarDisciplinaForm(FlaskForm):

    nome = StringField("Nome da disciplina:")
    submit = SubmitField("Buscar")

class EditarDisciplinaForm(FlaskForm):

    novo_nome = StringField("Novo nome:", validators=[DataRequired()])
    submit = SubmitField("Editar")

class ExcluirDisciplinaForm(FlaskForm):
    motivo = StringField("Motivo da exclusão por favor:")
    submit = SubmitField("Excluir")