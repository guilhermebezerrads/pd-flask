from flask import render_template, Blueprint, url_for, redirect, flash
from compleaks import db
from compleaks.arquivos.forms import (AdicionarArquivoForm, AdicionarDisciplinaForm,
					BuscarMaterialForm, EditarDisciplinaForm, EditarArquivoForm)

arquivos = Blueprint('arquivos', __name__,template_folder='templates/arquivos')

@arquivos.route('/adicionar', methods=['POST', 'GET'])
def adicionar():
    form_add = AdicionarArquivoForm()

    return render_template('adicionar_arquivo.html', form_add=form_add)

@arquivos.route('/editar', methods=['POST', 'GET'])
def editar():
	form = EditarArquivoForm()

	return render_template('editar_arquivo.html', form=form)

@arquivos.route('/listar', methods=['POST', 'GET'])
def listar():
	pass

@arquivos.route('/buscar', methods=['POST', 'GET'])
def buscar():

	form = BuscarMaterialForm()

	if form.validate_on_submit():

		return redirect(url_for('verconsulta'))

	return render_template('buscar.html', form=form)

@arquivos.route('/excluir', methods=['POST', 'GET'])
def excluir():
	pass

@arquivos.route('/adicionar-disciplina', methods=['POST', 'GET'])
def adicionar_disciplina():
	form = AdicionarDisciplinaForm()

	if form.validate_on_submit():
		nome = form.nome.data
		nova_disciplina = Disciplina(nome)

		db.session.add(nova_disciplina)
		db.session.commit()

		flash("A disciplina foi adicionada com sucesso.")
		return redirect(url_for('listar_disciplinas'))

	return render_template('adicionar_disciplina.html', form=form)

@arquivos.route('/editar-disciplina', methods=['POST', 'GET'])
def editar_disciplina():
	form = EditarDisciplinaForm()

	if form.validate_on_submit():
		id = form.id.data
		disciplina = Disciplina.query.get(id)
		disciplina.nome = form.nome.data

		db.session.add(disciplina)
		db.session.commit()

		flash("A disciplina foi editada com sucesso.")
		return redirect(url_for('listar_disciplinas'))

	return render_template('editar_disciplina.html', form=form)

@arquivos.route('/ver-consulta')
def ver_consulta():
    return render_template('ver_consulta.html')