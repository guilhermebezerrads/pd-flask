from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField,
                     SubmitField, SelectField)
from wtforms.validators import DataRequired, Email
from compleaks.professores.dapartamentos import lista_unidades_academicas

class AdicionarProfessorForm(FlaskForm):

    nome = StringField("Nome completo:", validators=[DataRequired()])
    unidade_academica = SelectField("Unidade Acadêmica: ", choices=lista_unidades_academicas(), validators=[DataRequired()])
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
    motivo_delete = StringField("Motivo da Exclusão:")
    submit = SubmitField("Excluir")