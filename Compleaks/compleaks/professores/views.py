from flask import render_template, Blueprint, url_for, redirect, flash, abort
from flask_login import current_user, login_required
from compleaks import db
from compleaks.professores.forms import (AdicionarProfessorForm, BuscarProfessorForm, EditarProfessorForm, 
										ExcluirProfessorForm)
from compleaks.professores.models import Professor
from datetime import datetime
from compleaks.professores.dapartamentos import lista_unidades_academicas
from compleaks.usuarios.forms import LoginForm

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

@professores.route('/listar')
def listar():
	form_excluir = ExcluirProfessorForm()
	form_editar = EditarProfessorForm()
	form_buscar = BuscarProfessorForm()
	form_login = LoginForm()
	professoresdb = Professor.query.order_by(Professor.nome.asc())

	return render_template('listar_professor.html', professoresdb=professoresdb, 
	lista = lista_unidades_academicas(), form_login=form_login, form_excluir=form_excluir, 
	form_editar=form_editar, form_buscar=form_buscar)

@professores.route('/buscar', methods=['POST', 'GET'])
def buscar():

	form_login = LoginForm()
	form_excluir = ExcluirProfessorForm()
	form_editar = EditarProfessorForm()
	form_buscar = BuscarProfessorForm()
	professoresdb = None
	existe_professor = False
	busca = False

	if form_buscar.validate_on_submit():
		busca=True
		nome = form_buscar.nome.data
		if nome == None:
			professoresdb = Professor.query.order_by(Professor.nome.asc())
		else:
			existe_professor = Professor.query.filter(Professor.nome.contains(nome)).first()
			professoresdb = Professor.query.filter(Professor.nome.contains(nome))
	
	return render_template('listar_professor.html', form_buscar=form_buscar, professoresdb=professoresdb, 
	existe_professor=existe_professor, form_login=form_login, busca=busca, lista = lista_unidades_academicas(),
	form_excluir=form_excluir, form_editar=form_editar)

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