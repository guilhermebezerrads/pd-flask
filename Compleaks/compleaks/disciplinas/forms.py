from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SubmitField)
from wtforms.validators import DataRequired, Length

class AdicionarDisciplinaForm(FlaskForm):

    nome = StringField("Nome da disciplina:", validators=[DataRequired()])
    submit = SubmitField("Adicionar")

class BuscarDisciplinaForm(FlaskForm):

    nome = StringField("Nome da disciplina:", validators=[DataRequired()])
    submit = SubmitField("Buscar")

class EditarDisciplinaForm(FlaskForm):

    id = IntegerField("Id da disciplina:", validators=[DataRequired()])
    novo_nome = StringField("Novo nome:", validators=[DataRequired()])
    submit = SubmitField("Editar")

class ExcluirDisciplinaForm(FlaskForm):

    id = IntegerField("Id da disciplina:", validators=[DataRequired()])
    motivo = StringField("Motivo da exclusão pro favor:")
    submit = SubmitField("Excluir")