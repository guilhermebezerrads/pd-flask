from flask import render_template, Blueprint, url_for, redirect, flash, abort, request
from flask_login import current_user, login_required
from compleaks import db, dist
from compleaks.questoes.forms import (ComentarioQuestaoForm, ExcluirComentarioQuestaoForm,
									 EditarComentarioQuestaoForm, ResponderComentarioQuestaoForm)
from compleaks.professores.forms import (AdicionarProfessorForm, BuscarProfessorForm, EditarProfessorForm, 
										ExcluirProfessorForm)
from compleaks.professores.models import Professor, ComentarioProf
from compleaks.arquivos.models import Arquivo
from datetime import datetime
from compleaks.professores.dapartamentos import lista_unidades_academicas
from compleaks.usuarios.forms import LoginForm
from compleaks.usuarios.models import Usuario

professores = Blueprint('professores', __name__,template_folder='templates/professores')

@professores.route('/adicionar', methods=['POST', 'GET'])
@login_required
def adicionar():

	if not current_user.is_authenticated:
		abort(403)
	form = AdicionarProfessorForm()

	if form.validate_on_submit():
		nome = form.nome.data
		unidade_academica = int(form.unidade_academica.data)
		novo_prof = Professor(nome, unidade_academica, current_user.id)
		db.session.add(novo_prof)
		db.session.commit()

		return redirect(url_for('professores.listar'))

	return render_template('adicionar_professor.html', form=form)
@professores.route('/lista/<nome>')
@professores.route('/listar', defaults={"nome":None},)
def listar(nome):
	form_excluir = ExcluirProfessorForm()
	form_editar = EditarProfessorForm()
	form_buscar = BuscarProfessorForm()
	form_login = LoginForm()

	page = request.args.get('page', 1, type=int)

	if not nome:
		professoresdb = Professor.query.order_by(Professor.nome.asc()).paginate(page=page, per_page=10)
	else:
		professoresdb = Professor.query.filter(Professor.nome.contains(nome))\
		.order_by(Professor.nome.asc()).paginate(page=page, per_page=10)

	professores = professoresdb
	professoresdb = professoresdb.items

	if professoresdb:
		existe_professor = True
	else:
		existe_professor = False

	return render_template('listar_professor.html', professoresdb=professoresdb, 
	lista = lista_unidades_academicas(), form_login=form_login, form_excluir=form_excluir, 
	form_editar=form_editar, form_buscar=form_buscar, professores=professores,
	 navigation_data=nome, existe_professor=existe_professor)

@professores.route('/buscar', methods=['POST', 'GET'])
def buscar():

	form_login = LoginForm()
	form_excluir = ExcluirProfessorForm()
	form_editar = EditarProfessorForm()
	form_buscar = BuscarProfessorForm()
	professoresdb = None
	existe_professor = False
	busca = False
	nome = None
	professores = None

	if form_buscar.validate_on_submit():
		busca=True
		nome = form_buscar.nome.data
		if nome == None:
			professoresdb = Professor.query.order_by(Professor.nome.asc()).paginate(page=page, per_page=10)
		else:
			existe_professor = Professor.query.filter(Professor.nome.contains(nome)).first()
			professoresdb = Professor.query.filter(Professor.nome.contains(nome)).paginate(page=page, per_page=10)

	else:
		return redirect(url_for('professoresdb.listar'))


	if existe_professor:
		professores = professoresdb
		professoresdb = professoresdb.items

	'''
	try:
		professoresdb = professoresdb.items
	except:
		professoresdb = []
		professores.iter_pages = Afs()
	'''
	return render_template('listar_professor.html', form_buscar=form_buscar, professoresdb=professoresdb, 
	existe_professor=existe_professor, form_login=form_login, busca=busca, lista = lista_unidades_academicas(),
	form_excluir=form_excluir, form_editar=form_editar, professores=professores, navigation_data=nome)

def Afs(left_edge=1, right_edge=1, left_current=1, right_current=2):
	lista = []
	return lista

@professores.route('/redefinir/<int:prof_id>', methods=['POST', 'GET'])
@login_required
def redefinir(prof_id):
	if not current_user.is_admin:
		abort(403)
	professor = Professor.query.get(prof_id)
	professor.ativado = True
	professor.data_deletado = None
	professor.id_deletor = None
	professor.motivo_delete = None

	db.session.commit()
	flash(f"Professor {professor.nome} foi restaurado no sistema.", "success")
	return redirect(url_for('professores.listar'))

@professores.route('/excluir/<int:prof_id>', methods=['POST', 'GET'])
@login_required
def excluir(prof_id):
	professor = Professor.query.get(prof_id)
	if not (current_user.is_admin or current_user.id==professor.id_criador):
		abort(403)

	form_excluir = ExcluirProfessorForm()

	if form_excluir.validate_on_submit():
		prof = Professor.query.get_or_404(prof_id)
		prof.id_deletor = current_user.id
		prof.ativado = False
		prof.data_deletado = datetime.now()
		prof.motivo_delete = form_excluir.motivo_delete.data
		db.session.commit()
		flash("O professor {} foi excluido com sucesso!".format(professor.nome),"success")
	return redirect(url_for('professores.listar', form_excluir=form_excluir))

@professores.route('/editar/<int:prof_id>', methods=['POST', 'GET'])
@login_required
def editar(prof_id):
	id = prof_id
	professor = Professor.query.get(id)
	if not (current_user.is_admin or current_user.id==professor.id_criador):
		abort(403)

	form_editar = EditarProfessorForm()

	if form_editar.validate_on_submit():		
		novo_nome = form_editar.novo_nome.data
		nova_unidade = int(form_editar.nova_unidade.data)
		Professor.query.filter_by(id=id).update(dict(nome=novo_nome))
		Professor.query.filter_by(id=id).update(dict(unidade_academica_id=nova_unidade))
		db.session.commit()
		flash("O tutor {} foi editado com sucesso!".format(professor.nome),"success")

	return redirect(url_for('professores.listar', form_editar=form_editar))

@professores.route('/perfil/<int:id>', methods=['POST', 'GET'])
@login_required
def perfil(id):
	page = request.args.get('page', 1, type=int)
	professor = Professor.query.get_or_404(id)

	if not professor.ativado:
		if not current_user.is_admin:
			abort(403)

	arquivos_todos = Arquivo.query.filter_by(professor_id=professor.id)

	quantidade = len([arquiv for arquiv in arquivos_todos if arquiv.ativado])

		
	arquivos = Arquivo.query\
					.filter(Arquivo.professor_id\
					.contains(int(professor.id)))\
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

	try:
		respondido = request.args.get("respondido")
		if respondido:
			
			resposta = request.args.get("responder_comentario"+str(respondido))

			condicion = ComentarioProf.query.filter_by(usuario_id=current_user.id)\
						.filter_by(conteudo=resposta)\
						.filter_by(professor_id=professor.id).first()

			if not condicion:
				responde_comment = ComentarioProf(conteudo=str(resposta), professor_id=professor.id, usuario_id=current_user.id, respondeu_id=int(respondido))
				db.session.add(responde_comment)
				db.session.commit()
		
		else:
			print("Não to aqui")

	except:
		print("To aqui")
	
	if form_comentario.validate_on_submit():
		conteudo = form_comentario.conteudo.data

		condicion = ComentarioProf.query.filter_by(usuario_id=current_user.id)\
					.filter_by(conteudo=conteudo)\
					.filter_by(professor_id=professor.id).first()

		if not condicion:
			new_comment = ComentarioProf(conteudo=conteudo, professor_id=professor.id, usuario_id=current_user.id)
			print(new_comment)
			db.session.add(new_comment)
			db.session.commit()


	if form_editar_comentario.validate_on_submit():
		coment = ComentarioProf.query.get(form_editar_comentario.id_coment.data)
		coment.conteudo = form_editar_comentario.novo_conteudo.data
		db.session.commit()

	if form_excluir_comentario.validate_on_submit():
		comentario = ComentarioProf.query.get(form_excluir_comentario.id_comment.data)
		if comentario:
			comentars = ComentarioProf.query.filter_by(respondeu_id=comentario.id)
			for comen in comentars:
				db.session.delete(comen)

			db.session.delete(comentario)
			db.session.commit()

	comentarios = professor.comentarios	

	return render_template('perfil_professor.html', professor=professor,
							arquivos=arquivos, arquivos_rows=arquivos_rows, dist=dist,
							contribuiu=quantidade, usuarios=usuarios, comentarios=comentarios,
							form_comentario=form_comentario, existe_arquivo=bool(contador),
							form_excluir_comentario=form_excluir_comentario,
							form_editar_comentario=form_editar_comentario )