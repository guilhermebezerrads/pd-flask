from flask import (render_template, Blueprint, url_for, redirect,
 					flash, current_app, request, abort)
from compleaks import db
from flask_login import current_user, login_required
from compleaks.disciplinas.models import Disciplina
from compleaks.usuarios.models import Usuario
from compleaks.questoes.models import  Questao, Alternativa, Comentario
from compleaks.questoes.forms import AdicionarQuestaoForm, BuscarQuestaoForm, FazerQuestaoForm, ComentarioQuestaoForm, ExcluirComentarioQuestaoForm, EditarComentarioQuestaoForm

questoes = Blueprint('questoes', __name__,template_folder='templates/questoes')

@questoes.route('/adicionar', methods=['POST', 'GET'])
@login_required
def adicionar():
	if not (current_user.is_authenticated):
		abort(403)
	form = AdicionarQuestaoForm()

	form.disciplina.choices = [(str(disciplina.id), disciplina.nome)
									 for disciplina in Disciplina.query.order_by('nome')
									 if disciplina.ativado]

	if form.validate_on_submit():

		#dados gerais
		disciplina = int(form.disciplina.data)
		enunciado = form.enunciado.data
		correta = int(form.correta.data)

		new_quest = Questao(enunciado=enunciado, disciplina_id=disciplina,
		 					usuario_id=current_user.id, correta=correta)

		db.session.add(new_quest)
		db.session.commit()

		quest = Questao.query.order_by(Questao.data_criacao.desc()).first()

		#alternativa a)
		conteudo = form.opcao_a.data
		alter_a = Alternativa(conteudo=conteudo, questao_id=quest.id, opcao=1)

		#alternativa b)
		conteudo = form.opcao_b.data
		alter_b = Alternativa(conteudo=conteudo, questao_id=quest.id, opcao=2)

		#alternativa c)
		conteudo = form.opcao_c.data
		alter_c = Alternativa(conteudo=conteudo, questao_id=quest.id, opcao=3)

		#alternativa d)
		conteudo = form.opcao_d.data
		alter_d = Alternativa(conteudo=conteudo, questao_id=quest.id, opcao=4)

		db.session.add_all([alter_d, alter_c, alter_b, alter_a])
		db.session.commit()

		flash("Questao cadastrada com sucesso", "success")

	return render_template('adicionar_questao.html', form=form)

@questoes.route('/buscar', methods=['POST', 'GET'])
@login_required
def buscar():
	if not (current_user.is_authenticated):
		abort(403)
	contador = {}
	form_buscar = BuscarQuestaoForm()
	questoes = Questao.query.order_by(Questao.data_criacao.desc())

	comment = [comentario.questao_id
									 for comentario in Comentario.query.order_by('questao_id')]
	comentarios = list(set(comment))
	for coment in comentarios:
		contador.update({str(coment):comment.count(coment)})
	alternativas = Alternativa.query.order_by(Alternativa.id.asc())
	busca = False
	existe_questao = False
	form_buscar.disciplina.choices = [(str(disciplina.id), disciplina.nome)
									 for disciplina in Disciplina.query.order_by('nome')
									 if disciplina.ativado]
	disciplinas = [(str(disciplina.id), disciplina.nome)
									 for disciplina in Disciplina.query.order_by('id')
									 if disciplina.ativado]
	
	if form_buscar.validate_on_submit():
		busca = True
		disc = form_buscar.disciplina.data
		enun = form_buscar.enunciado.data
		
		if enun=="":
			existe_questao = Questao.query.filter(Questao.disciplina_id.contains(disc)).first()
			questoes = Questao.query.filter(Questao.disciplina_id.contains(disc))
		else:
			query = db.session.query(Questao)
			query = Questao.query.filter(Questao.disciplina_id.contains(disc))
			query = Questao.query.filter(Questao.enunciado.contains(enun))
			questoes= query.all()
			existe_questao = query.all()

	return render_template('buscar_questao.html', questoes=questoes, alternativas=alternativas, disciplinas=disciplinas,
												 form_buscar=form_buscar, busca=busca, existe_questao=existe_questao,
												 comentarios=comentarios, contador=contador)

@questoes.route('/editar/<id>', methods=['POST', 'GET'])
@login_required
def editar(id):

	return render_template('editar_questao.html')

@questoes.route('/excluir/<id>', methods=['POST', 'GET'])
@login_required
def excluir(id):

	pass

@questoes.route('/restaurar/<id>', methods=['POST', 'GET'])
@login_required
def restaurar(id):

	pass

@questoes.route('/ver-questao/<int:id>', methods=['POST', 'GET'])
@login_required
def ver(id):
	if not (current_user.is_authenticated):
		abort(403)
	form_questao = FazerQuestaoForm() 
	form_comentario = ComentarioQuestaoForm()
	form_excluir_comentario = ExcluirComentarioQuestaoForm()
	form_editar_comentario = EditarComentarioQuestaoForm()
	usuarios = Usuario.query.all()
	questoes = Questao.query.filter(Questao.id.contains(id))
	alternativas = Alternativa.query.filter(Alternativa.questao_id.contains(id))
	form_questao.radio_alternativas.choices = [(str(alternativa.opcao), alternativa.conteudo)
									 for alternativa in Alternativa.query.filter(Alternativa.questao_id.contains(id))]
	for quest in questoes:
		usuario = Usuario.query.get(quest.usuario_id)
		disciplina = Disciplina.query.get(quest.disciplina_id)
		comentarios = Comentario.query.filter(Comentario.questao_id.contains(quest.id))
		if form_questao.validate_on_submit():
			if int(quest.correta)==int(form_questao.radio_alternativas.data):
				flash("Alternativa correta, meus parabens!", "success")
			else:
				flash("Alternativa errada, tente novamente!", "danger")	

		if form_comentario.validate_on_submit():
			conteudo = form_comentario.conteudo.data
			questao_id = quest.id
			new_comment = Comentario(conteudo=conteudo, questao_id=questao_id, usuario_id=current_user.id)
			db.session.add(new_comment)
			db.session.commit()

		if form_editar_comentario.validate_on_submit():
			coment = Comentario.query.get(form_editar_comentario.id_coment.data)
			coment.conteudo = form_editar_comentario.novo_conteudo.data
			db.session.commit()

		if form_excluir_comentario.validate_on_submit():
			comentario = Comentario.query.get(form_excluir_comentario.id_comment.data)
			if comentario:
				db.session.delete(comentario)
				db.session.commit()

	return render_template('ver_questao.html',usuario=usuario, disciplina = disciplina, questoes=questoes, 
	alternativas=alternativas, form_questao=form_questao, form_comentario=form_comentario,
	comentarios=comentarios, usuarios=usuarios, form_excluir_comentario=form_excluir_comentario,
	form_editar_comentario=form_editar_comentario)


@questoes.route('/redefinir/<int:id>', methods=['POST', 'GET'])
@login_required
def redefinir(id):
	if not current_user.is_admin:
		abort(403)

	quest = Questao.query.get(id)

@questoes.route('/excluidas', methods=['POST', 'GET'])
@login_required
def excluidas():
	if not current_user.is_admin:
		abort(403)

	questoes = Questao.query.filter_by(ativado=0)	

	return render_template('excluidas_questoes.html', questoes=questoes)
