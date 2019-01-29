from flask import render_template, Blueprint, url_for, redirect, flash
from compleaks import db
from compleaks.disciplinas.forms import (AdicionarDisciplinaForm, BuscarDisciplinaForm, EditarDisciplinaForm, ExcluirDisciplinaForm)
from compleaks.disciplinas.models import Disciplina

disciplinas = Blueprint('disciplinas', __name__,template_folder='templates/disciplinas')

@disciplinas.route('/adicionar', methods=['POST', 'GET'])
def adicionar():

	form = AdicionarDisciplinaForm()

	if form.validate_on_submit():
		nome = form.nome.data
		nova_disciplina = Disciplina(nome)
		db.session.add(nova_disciplina)
		db.session.commit()

		return redirect(url_for('disciplinas.listar'))

	return render_template('adicionar_disciplina.html', form=form)

@disciplinas.route('/editar', methods=['POST', 'GET'])
def editar():

	form = EditarDisciplinaForm()

	if form.validate_on_submit():
		id = form.id.data
		novo_nome = form.novo_nome.data
		Disciplina.query.filter_by(id=id).update(dict(nome=novo_nome))
		db.session.commit()

		return redirect(url_for('disciplinas.listar'))
	return render_template('editar_disciplina.html',form=form)

@disciplinas.route('/listar', methods=['POST', 'GET'])
def listar():

	disciplinadb = Disciplina.query.all()
	return render_template('listar_disciplina.html',disciplinadb=disciplinadb)

@disciplinas.route('/excluir', methods=['POST', 'GET'])
def excluir():

    form = ExcluirDisciplinaForm()

    if form.validate_on_submit():
        id = form.id.data
        disciplina = Disciplina.query.get(id)
        db.session.delete(disciplina)
        db.session.commit()

        return redirect(url_for('disciplinas.listar'))
    return render_template('excluir_disciplina.html',form=form)

@disciplinas.route('/buscar', methods=['POST', 'GET'])
def buscar():
	
	form = BuscarDisciplinaForm()

	if form.validate_on_submit():
		
		nome = form.nome.data
		existe_disciplina = Disciplina.query.filter(Disciplina.nome.contains(nome)).first()
		disciplinas = Disciplina.query.filter(Disciplina.nome.contains(nome))
		
		return render_template('resultado_busca.html',disciplinas=disciplinas , existe_disciplina=existe_disciplina)	

	return render_template('buscar_disciplina.html',form=form)