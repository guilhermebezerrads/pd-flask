from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import current_user, login_required
from compleaks import db
from compleaks.professores.forms import (AdicionarProfessorForm, BuscarProfessorForm, EditarProfessorForm, ExcluirProfessorForm)
from compleaks.professores.models import Professor
from datetime import datetime

professores = Blueprint('professores', __name__,template_folder='templates/professores')

@professores.route('/adicionar', methods=['POST', 'GET'])
@login_required
def adicionar():

	form = AdicionarProfessorForm()

	if form.validate_on_submit():
		nome = form.nome.data
		unidade_academica = int(form.unidade_academica.data)
		novo_prof = Professor(nome, unidade_academica)
		db.session.add(novo_prof)
		db.session.commit()

		return redirect(url_for('professores.listar'))

	return render_template('adicionar_professor.html', form=form)

@professores.route('/editar', methods=['POST', 'GET'])
@login_required
def editar():

	form = EditarProfessorForm()

	if form.validate_on_submit():
		id = form.id.data
		novo_nome = form.novo_nome.data
		Professor.query.filter_by(id=id).update(dict(nome=novo_nome))
		db.session.commit()

		return redirect(url_for('professores.listar'))
	return render_template('editar_professor.html',form=form)

@professores.route('/listar')
def listar():
	profdb = Professor.query.all()
	return render_template('listar_professor.html',profdb=profdb)

@professores.route('/excluir', methods=['POST', 'GET'])
@login_required
def excluir():
	form = ExcluirProfessorForm()
	
	if form.validate_on_submit():
		id = form.id.data
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
	
	form = BuscarProfessorForm()

	if form.validate_on_submit():
		
		nome = form.nome.data
		existe_professor = Professor.query.filter(Professor.nome.contains(nome)).first()
		professores = Professor.query.filter(Professor.nome.contains(nome))
		
		return render_template('resultado_busca.html',professores=professores , existe_professor=existe_professor)	

	return render_template('buscar_professor.html',form=form)