from flask import render_template, Blueprint, url_for, redirect, flash, abort
from flask_login import current_user, login_required
from compleaks import db
from compleaks.professores.forms import (AdicionarProfessorForm, BuscarProfessorForm, EditarProfessorForm, EditarProfessorUserForm, ExcluirProfessorForm)
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

@professores.route('/editar', methods=['POST', 'GET'])
@login_required
def editar():

	if not (current_user.is_admin or current_user.is_authenticated):
		abort(403)

	form = EditarProfessorForm()

	if form.validate_on_submit():
		id = form.id.data
		professor = Professor.query.get(id)
		if not (current_user.is_admin or current_user.id==professor.id_criador):
			abort(403)
		novo_nome = form.novo_nome.data
		nova_unidade = int(form.nova_unidade.data)
		Professor.query.filter_by(id=id).update(dict(nome=novo_nome))
		Professor.query.filter_by(id=id).update(dict(unidade_academica_id=nova_unidade))
		db.session.commit()

		return redirect(url_for('professores.listar'))
	return render_template('editar_professor.html',form=form)

@professores.route('/listar')
def listar():

	form_login = LoginForm()
	professoresdb = Professor.query.order_by(Professor.nome.asc())
	if current_user.is_authenticated and current_user.is_admin:
		return render_template('listar_professor.html', professoresdb=professoresdb, lista = lista_unidades_academicas(), form_login=form_login)
	else:
		return render_template('listar_professor_out.html',professoresdb=professoresdb, lista = lista_unidades_academicas(), form_login=form_login)

@professores.route('/excluir', methods=['POST', 'GET'])
@login_required
def excluir():
	if not (current_user.is_admin or current_user.is_authenticated):
		abort(403)

	form = ExcluirProfessorForm()

	if form.validate_on_submit():
		id = form.id.data
		professor = Professor.query.get(id)
		if not (current_user.is_admin or current_user.id==professor.id_criador):
			abort(403)
		prof = Professor.query.get_or_404(id)
		prof.id_deletor = current_user.id
		prof.is_eligible = False
		prof.data_deletado = datetime.now()
		prof.motivo_delete = form.motivo_delete.data
		db.session.commit()

		return redirect(url_for('professores.listar'))

	return render_template('excluir_professor.html',form=form)

@professores.route('/buscar', methods=['POST', 'GET'])
def buscar():

	form_login = LoginForm()
	form = BuscarProfessorForm()

	if form.validate_on_submit():

		nome = form.nome.data
		existe_professor = Professor.query.filter(Professor.nome.contains(nome)).first()
		professores = Professor.query.filter(Professor.nome.contains(nome))

		if current_user.is_authenticated and current_user.is_admin:
			return render_template('resultado_busca.html',professores=professores , existe_professor=existe_professor, lista = lista_unidades_academicas(), form_login=form_login)
		else:
			return render_template('resultado_busca_out.html',professores=professores , existe_professor=existe_professor, lista = lista_unidades_academicas(), form_login=form_login)
	
	return render_template('buscar_professor.html',form=form, form_login=form_login)

@professores.route('/redefinir/<int:prof_id>', methods=['POST', 'GET'])
@login_required
def redefinir(prof_id):
	if not current_user.is_admin:
		abort(403)
	professor = Professor.query.get(prof_id)
	professor.is_eligible = True
	professor.data_deletado = None
	professor.id_deletor = None
	professor.motivo_delete = None

	db.session.commit()
	flash(f"Professor {professor.nome} foi restaurado no sistema.", "success")
	return redirect(url_for('professores.listar'))

@professores.route('/user_excluir/<int:prof_id>,<motivo_delete>', methods=['POST', 'GET'])
@login_required
def user_excluir(prof_id, motivo_delete):

	professor = Professor.query.get(prof_id)

	if not (current_user.is_admin or (current_user.id == professor.id_criador)):
		abort(403)

	professor.is_eligible = False
	professor.data_deletado = datetime.now()
	professor.id_deletor = current_user.id
	professor.motivo_delete = motivo_delete

	db.session.commit()

	flash(f"Professor {professor.nome} foi excluido do sistema.", "success")
	return redirect(url_for('professores.listar'))

@professores.route('/user_editar/<int:prof_id>', methods=['POST', 'GET'])
@login_required
def user_editar(prof_id):

	professor = Professor.query.get(prof_id)

	if not (current_user.is_admin or current_user.is_authenticated):
		abort(403)

	form = EditarProfessorUserForm()
	
	id = prof_id

	if form.submit.data:
		if not (current_user.is_admin or current_user.id==professor.id_criador):
			abort(403)
		novo_nome = form.novo_nome.data
		nova_unidade = int(form.nova_unidade.data)
		Professor.query.filter_by(id=id).update(dict(nome=novo_nome))
		Professor.query.filter_by(id=id).update(dict(unidade_academica_id=nova_unidade))
		db.session.commit()
		flash(f"Professor {professor.nome} foi editado no sistema.", "success")
		return redirect(url_for('professores.listar'))

	return render_template('editar_professor_user.html',form=form)