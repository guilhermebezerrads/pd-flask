from flask import (render_template, Blueprint, url_for, redirect, flash, abort)
from flask_login import current_user, login_required
from compleaks import db
from compleaks.disciplinas.forms import (AdicionarDisciplinaForm, BuscarDisciplinaForm, EditarDisciplinaForm, ExcluirDisciplinaForm)
from compleaks.disciplinas.models import Disciplina
from compleaks.usuarios.forms import LoginForm
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
	disciplina = Disciplina.query.get(disc_id)
	if not (current_user.is_admin or current_user.id==disciplina.id_criador):
		abort(403)

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
	
	id = disc_id
	disciplina = Disciplina.query.get(id)
	if not (current_user.id==disciplina.id_criador):
		abort(403)

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