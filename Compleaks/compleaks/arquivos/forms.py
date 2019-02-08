from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import (StringField, IntegerField, SubmitField, 
	TextField, SelectField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length
from compleaks.arquivos.preenche_select import Preenche


class BuscarMaterialForm(FlaskForm):

	selecteds = Preenche()
	professor = StringField("Digite o nome do professor:")
	disciplina = StringField("Digite o nome da disciplina:")
	filtrar = SelectField("Pesquisar por", choices=[('0','Todos'),('1','Disciplina'),
												('2','Professor'), ('3','Tipo de Arquivo')])
	tipo_arquivo = SelectField("Tipo do arquivo", choices=[('all','todos'), 
		('apostila','Apostila'),
		('slide','Apresentação/Slides'),('lista','Lista de exercícios'),
		('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')])
	submit = SubmitField("Buscar")


class AdicionarArquivoForm(FlaskForm):

	selecteds = Preenche()
	ano = SelectField("Ano de referência do conteúdo", choices=[('2010','A'),('2110','B')])
	semestre = SelectField("Semestre de referência", choices=[('1','1°'),('2','2°')], 
		validators=[DataRequired()])
	tipo_conteudo = SelectField("Tipo do conteúdo", choices=[('apostila','Apostila'),
		('slide','Apresentação/Slides'),('lista','Lista de exercícios'),
		('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')], 
		validators=[DataRequired()])
	observacoes = TextField("Observações", validators=[DataRequired(), 
		Length(min=10, max=120, message="Minimo de 10 caracteres e máximo de 120 por favor!")])
	arquivo = FileField("Arquivo", validators=[DataRequired(), 
		FileAllowed(['jpg', 'png', 'pdf', 'bmp' , 'jpeg', 'gif'])])

	submit = SubmitField("Adicionar")

class EditarArquivoForm(FlaskForm):

	selecteds = Preenche()

	ano = SelectField("Ano de referência do conteúdo", choices=[('2010','A'),('2110','B')])	
	semestre = SelectField("Semestre de referência", choices=[('1','1°'),('2','2°')], 
		validators=[DataRequired()])
	tipo_conteudo = SelectField("Tipo do conteúdo", choices=[('apostila','Apostila'),
		('slide','Apresentação/Slides'),('lista','Lista de exercícios'),
		('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')], 
		validators=[DataRequired()])	
	observacoes = TextField("Observações", validators=[DataRequired(), 
		Length(min=10, max=120, message="Minimo de 10 caracteres e máximo de 120 por favor!")])

	submit = SubmitField("Atualizar")
