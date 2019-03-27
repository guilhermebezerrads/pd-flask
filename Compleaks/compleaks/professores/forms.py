from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField,
                     SubmitField, SelectField, TextAreaField)
from wtforms.validators import DataRequired, Email
from compleaks.professores.dapartamentos import lista_unidades_academicas

class AdicionarProfessorForm(FlaskForm):

    nome = StringField("Nome completo:", validators=[DataRequired()])
    unidade_academica = SelectField("Unidade Acadêmica: ", choices=lista_unidades_academicas(), validators=[DataRequired()])
    submit = SubmitField("Adicionar")

class BuscarProfessorForm(FlaskForm):

    nome = StringField("Nome do professor:")
    submit = SubmitField("Buscar")

#Formularios ativos para excluir e adicionar usando apenas a pagina de listar por meio da modal
class ExcluirProfessorForm(FlaskForm):

    motivo_delete = StringField("Motivo da Exclusão:")
    submit = SubmitField("Excluir")

class EditarProfessorForm(FlaskForm):

    novo_nome = StringField("Novo nome completo:", validators=[DataRequired()])
    nova_unidade = SelectField("Nova Unidade Acadêmica: ", choices=lista_unidades_academicas(), validators=[DataRequired()])
    submit = SubmitField("Editar")
