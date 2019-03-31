from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, BooleanField, SelectField, TextAreaField, RadioField, IntegerField)
from wtforms.validators import DataRequired, Length

class AdicionarQuestaoForm(FlaskForm):	

	enunciado = TextAreaField("Enunciado:", validators=[DataRequired(), 
				Length( max=400, message="Máximo de 400 por favor!")])
	disciplina = SelectField("Disciplina:", validators=[DataRequired()])
	materia = SelectField("Materia:", validators=[DataRequired()])
	correta = SelectField("Correta:", validators=[DataRequired()],
				 choices=[("1","a)"), ("2","b)"), ("3","c)"),("4","d)")])
	opcao_a = StringField("a)", validators=[DataRequired(), 
			Length(min=4, max=120, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	opcao_b = StringField("b)", validators=[DataRequired(),
		Length(min=4, max=120, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	opcao_c = StringField("c)", validators=[DataRequired(),
			Length(min=4, max=120, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	opcao_d = StringField("d)", validators=[DataRequired(),
			Length(min=4, max=120, message="Minimo de 4 caracteres e máximo de 120 por favor!")])
	submit = SubmitField("Adicionar")
	

class EditarQuestaoForm(FlaskForm):
	enunciado = StringField("Enunciado:", validators=[DataRequired()])
	disciplina = SelectField("Disciplina:", validators=[DataRequired()])
	correta = SelectField("Correta:", validators=[DataRequired()],
				 choices=[(1,"a"), (2,"b"), (3,"c"),(4,"d")])
	opcao_a = StringField("a)", validators=[DataRequired()])
	opcao_b = StringField("b)", validators=[DataRequired()])
	opcao_c = StringField("c)", validators=[DataRequired()])
	opcao_d = StringField("d)", validators=[DataRequired()])
	submit = SubmitField("Adicionar")

class BuscarQuestaoForm(FlaskForm):
	disciplina = SelectField("Selecione a disciplina que deseja buscar", validators=[DataRequired()])
	enunciado = StringField("Enunciado:")
	submit = SubmitField("Buscar")

class FazerQuestaoForm(FlaskForm):
	radio_alternativas = RadioField("Selecione a resposta correta", validators=[DataRequired()])
	submit = SubmitField("Pronto")

class ComentarioQuestaoForm(FlaskForm):
	conteudo = TextAreaField("Conteudo", validators=[DataRequired()])
	comentar = SubmitField("Comentar")

class ExcluirComentarioQuestaoForm(FlaskForm):
	id_comment = IntegerField("Id do comentario:", validators=[DataRequired()])
	excluir = SubmitField("Excluir")

class EditarComentarioQuestaoForm(FlaskForm):
	id_coment = IntegerField("Id do comentario:", validators=[DataRequired()])
	novo_conteudo = TextAreaField("Conteudo", validators=[DataRequired()])
	submit = SubmitField("Editar")

class ResponderComentarioQuestaoForm(FlaskForm):
	conteudo = TextAreaField("Conteudo", validators=[DataRequired()])
	respondeu_id = IntegerField("Id do comentario a ser respondido")
	submit = SubmitField("Responder")
