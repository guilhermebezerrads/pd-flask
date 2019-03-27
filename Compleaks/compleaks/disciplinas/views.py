from flask import (render_template, Blueprint, url_for, redirect, flash, abort)
from flask_login import current_user, login_required
from compleaks import db
from compleaks.disciplinas.forms import (AdicionarDisciplinaForm, BuscarDisciplinaForm, EditarDisciplinaForm, ExcluirDisciplinaForm)
from compleaks.disciplinas.models import Disciplina, ComentarioDisc
from compleaks.usuarios.forms import LoginForm
from compleaks.usuarios.models import Usuario
from datetime import datetime

disciplinas = Blueprint('disciplinas', __name__,template_folder='templates/disciplinas')

@disciplinas.route('/adicionar', methods=['POST', 'GET'])
@login_required
def adicionar():

	if not current_user.is_admin:
		abort(403)

	form = AdicionarDisciplinaForm()

	if form.validate_on_submit():
		nome = form.nome.data
		nova_disciplina = Disciplina(nome, current_user.id)
		db.session.add(nova_disciplina)
		db.session.commit()

		return redirect(url_for('disciplinas.listar'))

	return render_template('adicionar_disciplina.html', form=form)

@disciplinas.route('/listar', methods=['POST', 'GET'])
def listar():
	form_excluir = ExcluirDisciplinaForm()
	form_editar = EditarDisciplinaForm()
	form_buscar = BuscarDisciplinaForm()
	form_login = LoginForm()

	disciplinadb = Disciplina.query.order_by(Disciplina.nome.asc())

	return render_template('listar_disciplina.html',disciplinadb=disciplinadb, form_login=form_login,
							form_buscar=form_buscar, form_editar=form_editar, form_excluir=form_excluir)

@disciplinas.route('/buscar', methods=['POST', 'GET'])
def buscar():

	form_login = LoginForm()
	form_excluir = ExcluirDisciplinaForm()
	form_editar = EditarDisciplinaForm()
	form_buscar = BuscarDisciplinaForm()
	disciplinadb = None
	existe_disciplina = False
	busca = False

	if form_buscar.validate_on_submit():
		busca=True
		nome = form_buscar.nome.data		

		if nome == None:
			disciplinadb = Disciplina.query.order_by(Disciplina.nome.asc())
		else:
			existe_disciplina = Disciplina.query.filter(Disciplina.nome.contains(nome)).first()
			disciplinadb = Disciplina.query.filter(Disciplina.nome.contains(nome))
	
	return render_template('listar_disciplina.html', disciplinadb=disciplinadb, busca=busca, existe_disciplina=existe_disciplina,
	form_buscar=form_buscar, form_editar=form_editar, form_excluir=form_excluir, form_login=form_login)

@disciplinas.route('/excluir/<int:disc_id>', methods=['POST', 'GET'])
@login_required
def excluir(disc_id):

	if not (current_user.is_admin):
		abort(403)
		
	disciplina = Disciplina.query.get(disc_id)

	form_excluir = ExcluirDisciplinaForm()

	if form_excluir.validate_on_submit():
		disc = Disciplina.query.get_or_404(disc_id)
		disc.id_deletor = current_user.id
		disc.ativado = False
		disc.data_deletado = datetime.now()
		disc.motivo_delete = form_excluir.motivo.data
		db.session.commit()
		flash("A disciplina {} foi excluido com sucesso!".format(disciplina.nome),"success")

	return redirect(url_for('disciplinas.listar', form_excluir=form_excluir))

@disciplinas.route('/editar/<int:disc_id>', methods=['POST', 'GET'])
@login_required
def editar(disc_id):

	if not (current_user.is_admin):
		abort(403)

	
	id = disc_id
	disciplina = Disciplina.query.get(id)
	
	form_editar = EditarDisciplinaForm()

	if form_editar.validate_on_submit():
		novo_nome = form_editar.novo_nome.data
		#Disciplina.query.filter_by(id=id).update(dict(nome=novo_nome))
		disciplina = Disciplina.query.get(id)
		disciplina.nome = novo_nome
		db.session.commit()
	
	return redirect(url_for('disciplinas.listar', form_editar=form_editar))

@disciplinas.route('/redefinir/<int:disc_id>', methods=['POST', 'GET'])
@login_required
def redefinir(disc_id):
	if not current_user.is_admin:
		abort(403)
	disciplina = Disciplina.query.get(disc_id)
	disciplina.ativado = True
	disciplina.data_deletado = None
	disciplina.id_deletor = None
	disciplina.motivo_delete = None

	db.session.commit()
	flash(f"Disciplina {disciplina.nome} foi restaurada no sistema.", "success")
	return redirect(url_for('disciplinas.listar'))


@disciplinas.route('/perfil/<int:id>', methods=['POST', 'GET'])
@login_required
def perfil(id):

	disciplina = Disciplina.query.get_or_404(id)

	arquivos_todos = Arquivo.query.filter_by(disciplina_id=disciplina.id)

	quantidade = len([arquiv for arquiv in arquivos_todos if arquiv.ativado])

	page = request.args.get('page', 1, type=int)	
	arquivos = Arquivo.query\
					.filter(Arquivo.disciplina_id\
					.contains(int(disciplina.id)))\
					.filter_by(ativado=True)\
					.paginate(page=page, per_page=12)

	arquivos_row_1 = []
	arquivos_row_2 = []
	arquivos_row_3 = []
	contador = 0
	for arquivo in arquivos.items:
		if contador >= 4:
			break 
		arquivos_row_1.append(arquivo)
		contador = contador + 1

	contador = 0
	for arquivo in arquivos.items:
		if contador >= 8:
			break
		if contador >= 4:
			arquivos_row_2.append(arquivo)
		contador = contador + 1				

	contador = 0
	for arquivo in arquivos.items:
		if contador >= 12:
			break
		if contador >= 8:
			arquivos_row_3.append(arquivo)
		contador = contador + 1				

	arquivos_rows = [arquivos_row_1, arquivos_row_2, arquivos_row_3]

	for row in arquivos_rows:
		for arquivo in row:
			arquivo.avaliado = False

	if current_user.is_authenticated:
		for row in arquivos_rows:
			for arquivo in row:
				for avl in arquivo.avaliacoes:
					if avl in current_user.avaliacoes:
						arquivo.avaliado = True

	total = 0.0
	for row in arquivos_rows:
		for arquivo in row:
			total = 0.0
			if len(arquivo.avaliacoes): 
				for avl in arquivo.avaliacoes:
					total = total + avl.nota
				total = total/len(arquivo.avaliacoes)
			else:
				total = 0.0

			arquivo.nota_decimal = round(total, 1)

	'''Parte de Comentários'''

	form_comentario = ComentarioQuestaoForm()
	form_excluir_comentario = ExcluirComentarioQuestaoForm()
	form_editar_comentario = EditarComentarioQuestaoForm()

	usuarios = Usuario.query.all()

	comentarios = disciplina.comentarios	

	try:
		respondido = request.args.get("respondido")
		if respondido:
			
			resposta = request.args.get("responder_comentario"+str(respondido))

			condicion = ComentarioDisc.query.filter_by(usuario_id=current_user.id)\
						.filter_by(conteudo=resposta)\
						.filter_by(professor_id=professor.id).first()

			if not condicion:
				responde_comment = ComentarioDisc(conteudo=str(resposta), disciplina_id=disciplina.id, usuario_id=current_user.id, respondeu_id=int(respondido))
				db.session.add(responde_comment)
				db.session.commit()
		
		else:
			print("Não to aqui")

	except:
		print("To aqui")
	
	if form_comentario.validate_on_submit():
		conteudo = form_comentario.conteudo.data

		condicion = ComentarioDisc.query.filter_by(usuario_id=current_user.id)\
					.filter_by(conteudo=conteudo)\
					.filter_by(disciplina_id=disciplina.id).first()

		if not condicion:
			new_comment = ComentarioDisc(conteudo=conteudo, disciplina_id=disciplina.id, usuario_id=current_user.id)
			db.session.add(new_comment)
			db.session.commit()


	if form_editar_comentario.validate_on_submit():
		coment = ComentarioDisc.query.get(form_editar_comentario.id_coment.data)
		coment.conteudo = form_editar_comentario.novo_conteudo.data
		db.session.commit()

	if form_excluir_comentario.validate_on_submit():
		comentario = ComentarioDisc.query.get(form_excluir_comentario.id_comment.data)
		if comentario:
			comentars = ComentarioDisc.query.filter_by(respondeu_id=comentario.id)
			for comen in comentars:
				db.session.delete(comen)

			db.session.delete(comentario)
			db.session.commit()

	return render_template('perfil_professor_teste.html', disciplina=disciplina,
							arquivos=arquivos, arquivos_rows=arquivos_rows, dist=dist,
							contribuiu=quantidade, usuarios=usuarios, comentarios=comentarios,
							form_comentario=form_comentario, existe_arquivo=bool(contador),
							form_excluir_comentario=form_excluir_comentario,
							form_editar_comentario=form_editar_comentario)