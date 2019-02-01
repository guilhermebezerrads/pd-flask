from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import (StringField, IntegerField, SubmitField, 
	TextField, SelectField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length
from compleaks.arquivos.models import listaDiciplinas, listaProfessores


class BuscarMaterialForm(FlaskForm):

	disciplina = StringField("Disciplina")
	tipo_arquivo = SelectField("Tipo do arquivo", choices=[('apostila','Apostila'),
		('slide','Apresentação/Slides'),('lista','Lista de exercícios'),
		('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')])
	professor = StringField("Professor")
	submit = SubmitField("Buscar")


class AdicionarArquivoForm(FlaskForm):

	disciplina = SelectField("Diciplina do arquivo", choices=listaDiciplinas(), validators=[DataRequired()])
	ano = SelectField("Ano de referência do conteúdo", choices=[('2010','A'),('2110','B')])
	semestre = SelectField("Semestre de referência", choices=[('1','1°'),('2','2°')], 
		validators=[DataRequired()])
	tipo_conteudo = SelectField("Tipo do conteúdo", choices=[('apostila','Apostila'),
		('slide','Apresentação/Slides'),('lista','Lista de exercícios'),
		('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')], 
		validators=[DataRequired()])
	professor = SelectField("Nome do Professor", choices=listaProfessores(), validators=[DataRequired()])
	observacoes = TextField("Observações", validators=[DataRequired(), Length(min=10, max=120, message="Minimo de 10 caracteres e máximo de 120 por favor!")])
	arquivo = FileField("Arquivo", validators=[DataRequired(), FileAllowed(['jpg', 'png', 'pdf', 'bmp' , 'jpeg', 'gif'])])

	submit = SubmitField("Adicionar")

class EditarArquivoForm(FlaskForm):

	disciplina = SelectField("Diciplina do arquivo", choices=listaDiciplinas(), validators=[DataRequired()])	
	ano = SelectField("Ano de referência do conteúdo", choices=[('2010','A'),('2110','B')])	
	semestre = SelectField("Semestre de referência", choices=[('1','1°'),('2','2°')], 
		validators=[DataRequired()])
	tipo_conteudo = SelectField("Tipo do conteúdo", choices=[('apostila','Apostila'),
		('slide','Apresentação/Slides'),('lista','Lista de exercícios'),
		('prova','Prova'),('trabalho','Trabalho'),('outro','Outro')], 
		validators=[DataRequired()])
	professor = SelectField("Nome do Professor", choices=listaProfessores(), validators=[DataRequired()])	
	observacoes = TextField("Observações", validators=[DataRequired(), Length(min=10, max=120, message="Minimo de 10 caracteres e máximo de 120 por favor!")])

	submit = SubmitField("Atualizar")
