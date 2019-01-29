from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import (StringField, IntegerField, SubmitField, 
	TextField, SelectField, FileField)
from wtforms.validators import DataRequired

class AdicionarDisciplinaForm(FlaskForm):

	nome = StringField("Nome da disciplina")
	submit = SubmitField("Adicionar")


class EditarDisciplinaForm(FlaskForm):

	id = IntegerField("ID da disciplina a ser editada")
	nome = StringField("Novo nome")
	submit = SubmitField("Salvar")


class BuscarMaterialForm(FlaskForm):

	disciplina = StringField("Disciplina")
	tipo_arquivo = SelectField("Tipo do arquivo", choices=[('apostila','Apostila'),
		('slide','Apresentação/Slides'),('lista','Lista de exercícios'),
		('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')])
	professor = StringField("Professor")
	submit = SubmitField("Buscar")


class AdicionarArquivoForm(FlaskForm):

	disciplina = SelectField("Diciplina do arquivo", choices=[('a','A'),('b','B')])
	ano = SelectField("Ano de referência do conteúdo", choices=[('a','A'),('b','B')])
	semestre = SelectField("Semestre de referência", choices=[('1','1°'),('2','2°')], 
		validators=[DataRequired()])
	tipo_conteudo = SelectField("Tipo do conteúdo", choices=[('apostila','Apostila'),
		('slide','Apresentação/Slides'),('lista','Lista de exercícios'),
		('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')], 
		validators=[DataRequired()])
	professor = StringField("Nome do Professor", validators=[DataRequired()])
	observacoes = TextField("Observações", validators=[DataRequired()])
	arquivo = FileField("Arquivo", validators=[DataRequired()])

	submit = SubmitField("Adicionar")

class EditarArquivoForm(FlaskForm):

	disciplina = SelectField("Diciplina do arquivo", choices=[('a','A'),('b','B')])
	ano = SelectField("Ano de referência do conteúdo", choices=[('a','A'),('b','B')])
	semestre = SelectField("Semestre de referência", choices=[('1','1°'),('2','2°')], 
		validators=[DataRequired()])
	tipo_conteudo = SelectField("Tipo do conteúdo", choices=[('apostila','Apostila'),
		('slide','Apresentação/Slides'),('lista','Lista de exercícios'),
		('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')], 
		validators=[DataRequired()])
	professor = StringField("Nome do Professor", validators=[DataRequired()])
	observacoes = TextField("Observações", validators=[DataRequired()])

	submit = SubmitField("Atualizar")
