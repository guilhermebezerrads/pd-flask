from flask import (render_template, Blueprint, url_for, redirect,
 					flash, current_app, request, abort, Markup)
from compleaks import db
from flask_login import current_user, login_required
from compleaks.disciplinas.models import Disciplina, Materia
from compleaks.usuarios.models import Usuario
from compleaks.questoes.models import  Questao, Alternativa, Comentario
from compleaks.questoes.forms import AdicionarQuestaoForm, BuscarQuestaoForm, FazerQuestaoForm, ComentarioQuestaoForm, ExcluirComentarioQuestaoForm, EditarComentarioQuestaoForm, ResponderComentarioQuestaoForm

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
		materia_id = int(form.materia.data)

		new_quest = Questao(enunciado=enunciado, disciplina_id=disciplina,
		 					usuario_id=current_user.id, correta=correta,
		 					materia_id=materia_id)

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
	
	form_questao = FazerQuestaoForm(prefix="form_questao") 
	form_comentario = ComentarioQuestaoForm(prefix="form_comentario")
	form_excluir_comentario = ExcluirComentarioQuestaoForm(prefix="form_excluir_comentario")
	form_editar_comentario = EditarComentarioQuestaoForm(prefix="form_editar_comentario")
	form_responde_comentario = ResponderComentarioQuestaoForm(prefix="form_responde_comentario")

	usuarios = Usuario.query.all()
	quest = Questao.query.get(id)
	alternativas = Alternativa.query.filter(Alternativa.questao_id.contains(id))
	form_questao.radio_alternativas.choices = [(str(alternativa.opcao), alternativa.conteudo)
									 for alternativa in Alternativa.query.filter(Alternativa.questao_id.contains(id))]

	usuario = Usuario.query.get(quest.usuario_id)
	disciplina = Disciplina.query.get(quest.disciplina_id)
	comentarios = Comentario.query.filter(Comentario.questao_id.contains(quest.id)).order_by(Comentario.data_criacao.desc())	
	comentarios = comentarios.order_by('data_criacao')

	if form_responde_comentario.validate_on_submit() and form_responde_comentario.submit.data:
		conteudo = form_responde_comentario.conteudo.data
		respondeu_id = form_responde_comentario.respondeu_id.data
		questao_id = quest.id
		if(respondeu_id):
			responde_comment = Comentario(conteudo=conteudo, questao_id=questao_id, usuario_id=current_user.id, respondeu_id=respondeu_id)
			db.session.add(responde_comment)
			db.session.commit()

	if form_questao.validate_on_submit() and form_questao.submit.data:
		if int(quest.correta)==int(form_questao.radio_alternativas.data):
			flash("Alternativa correta, meus parabens!", "success")
		else:
			flash("Alternativa errada, tente novamente!", "danger")	

	if form_comentario.validate_on_submit() and form_comentario.comentar.data:
		conteudo = form_comentario.conteudo.data

		condicion = Comentario.query.filter_by(usuario_id=current_user.id)\
					.filter_by(conteudo=conteudo)\
					.filter_by(questao_id=quest.id).first()

		if not condicion:
			questao_id = quest.id
			new_comment = Comentario(conteudo=conteudo, questao_id=questao_id, usuario_id=current_user.id, respondeu_id=0)
			db.session.add(new_comment)
			db.session.commit()

	if form_excluir_comentario.validate_on_submit() and form_excluir_comentario.excluir.data:
		comentario = Comentario.query.get(form_excluir_comentario.id_comment.data)
		if comentario:
			comentars = Comentario.query.filter_by(respondeu_id=comentario.id)
			for comen in comentars:
				db.session.delete(comen)

			db.session.delete(comentario)
			db.session.commit()		

	if form_editar_comentario.is_submitted() and form_editar_comentario.submit.data:
		coment = Comentario.query.get(form_editar_comentario.id_coment.data)
		coment.conteudo = form_editar_comentario.novo_conteudo.data
		db.session.commit()

	return render_template('ver_questao.html',usuario=usuario, disciplina = disciplina, quest=quest, 
	alternativas=alternativas, form_questao=form_questao, form_comentario=form_comentario,
	comentarios=comentarios, usuarios=usuarios, form_excluir_comentario=form_excluir_comentario,
	form_editar_comentario=form_editar_comentario, form_responde_comentario=form_responde_comentario)



@questoes.route('/redefinir/<int:id>', methods=['POST', 'GET'])
@login_required
def redefinir(id):
	if not current_user.is_admin:
		abort(403)

	quest = Questao.query.get(id)
	quest.ativado = True
	db.session.commit()

	flash("Questao redefinida com sucesso", "success")

	return redirect(url_for('questoes.excluidas'))


@questoes.route('/excluidas', methods=['POST', 'GET'])
@login_required
def excluidas():
	if not current_user.is_admin:
		abort(403)

	contador = {}
	comment = [comentario.questao_id
									 for comentario in Comentario.query.order_by('questao_id')]
	comentarios = list(set(comment))
	print(comentarios)

	for coment in comentarios:
		contador.update({str(coment):comment.count(coment)})


	page = request.args.get('page', 1, type=int)
	questoes = Questao.query.filter_by(ativado=False).paginate(page=page, per_page=10)	

	alternativas = Alternativa.query.order_by(Alternativa.id.asc())

	return render_template('excluidas_questoes.html', questoes=questoes,
							 contador=contador, alternativas=alternativas)

'''Retronando a parte do formulário que tem as matérias relacionadas'''
@questoes.route('/materias/<int:id>', methods=['POST', 'GET'])
@login_required
def materias(id):

	form = AdicionarQuestaoForm()

	disciplina = Disciplina.query.get_or_404(id)
	materias = Materia.query.filter_by(disciplina_id=disciplina.id)

	form.materia.choices = []
	form.materia.choices.append(("0", "Sem materia relacionada"))
	form.materia.choices += [(str(materia.id), materia.nome) for materia in materias]

	return render_template('materias_relacionadas.html', form=form)