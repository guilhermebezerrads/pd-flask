from flask import (render_template, Blueprint, 
					url_for, redirect, flash, abort)
from flask_login import current_user, login_required
from compleaks import db
from compleaks.disciplinas.forms import (AdicionarDisciplinaForm, BuscarDisciplinaForm, 
										EditarDisciplinaForm, ExcluirDisciplinaForm)
from compleaks.disciplinas.models import Disciplina
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
		nova_disciplina = Disciplina(nome)
		db.session.add(nova_disciplina)
		db.session.commit()

		return redirect(url_for('disciplinas.listar'))

	return render_template('adicionar_disciplina.html', form=form)

@disciplinas.route('/editar', methods=['POST', 'GET'])
@login_required
def editar():
	if not current_user.is_admin:
		abort(403)
	form = EditarDisciplinaForm()

	if form.validate_on_submit():
		id = form.id.data
		novo_nome = form.novo_nome.data
		#Disciplina.query.filter_by(id=id).update(dict(nome=novo_nome))
		disciplina = Disciplina.query.get(id)

		if disciplina is None:
			flash("Id da disciplina inexistente!")
			return redirect(url_for('disciplinas.editar'))

		disciplina.nome = novo_nome
		db.session.commit()

		return redirect(url_for('disciplinas.listar'))
	return render_template('editar_disciplina.html',form=form)

@disciplinas.route('/listar', methods=['POST', 'GET'])
@login_required
def listar():
	if not current_user.is_admin:
		abort(403)
	disciplinadb = Disciplina.query.order_by(Disciplina.nome.desc())
	return render_template('listar_disciplina.html',disciplinadb=disciplinadb)

@disciplinas.route('/listar_ou', methods=['POST', 'GET'])
def listar_out():
	disciplinadb = Disciplina.query.order_by(Disciplina.nome.desc())
	return render_template('lista_disciplina_out.html',disciplinadb=disciplinadb)

@disciplinas.route('/excluir', methods=['POST', 'GET'])
@login_required
def excluir():
	if not current_user.is_admin:
		abort(403)
	form = ExcluirDisciplinaForm()

	if form.validate_on_submit():
		id = form.id.data
		disciplina = Disciplina.query.get(id)

		disciplina.is_eligible = False
		disciplina.data_deletado = datetime.now()
		disciplina.id_deletor = current_user.id
		disciplina.motivo_delete = form.motivo.data

		db.session.commit()

		return redirect(url_for('disciplinas.listar'))

	return render_template('excluir_disciplina.html',form=form)

@disciplinas.route('/redefinir/<int:disc_id>', methods=['POST', 'GET'])
@login_required
def redefinir(disc_id):
	if not current_user.is_admin:
		abort(403)
	disciplina = Disciplina.query.get(disc_id)
	disciplina.is_eligible = True
	disciplina.data_deletado = None
	disciplina.id_deletor = None
	disciplina.motivo_delete = None
		
	db.session.commit()
	flash("Disciplina {} acabou de redefinido ao sistema!".format(disciplina.nome))
	return redirect(url_for('disciplinas.listar'))

@disciplinas.route('/buscar', methods=['POST', 'GET'])
@login_required
def buscar():

	if not current_user.is_admin:
		abort(403)
	
	form = BuscarDisciplinaForm()

	if form.validate_on_submit():
		
		nome = form.nome.data
		existe_disciplina = Disciplina.query.filter(Disciplina.nome.	tains(nome)).first()
		disciplinas = Disciplina.query.filter(Disciplina.nome.contains(nome))
		
		return render_template('resultado_busca.html',disciplinas=disciplinas , existe_disciplina=existe_disciplina)	

	return render_template('buscar_disciplina.html',form=form)

@disciplinas.route('/buscar_out', methods=['POST', 'GET'])
def buscar_out():
	
	form = BuscarDisciplinaForm()

	if form.validate_on_submit():
		
		nome = form.nome.data
		existe_disciplina = Disciplina.query.filter(Disciplina.nome.contains(nome)).first()
		disciplinas = Disciplina.query.filter(Disciplina.nome.contains(nome))

		if current_user.is_authenticated:
			return render_template('resultado_busca.html',disciplinas=disciplinas , existe_disciplina=existe_disciplina)	
		else:
			return render_template('resultado_busca_out.html',disciplinas=disciplinas , existe_disciplina=existe_disciplina)	

	return render_template('buscar_disciplina.html',form=form)