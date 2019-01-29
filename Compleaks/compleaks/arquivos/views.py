from flask import render_template, Blueprint, url_for, redirect, flash, current_app
from compleaks import db
from flask_login import current_user, login_required
from compleaks.arquivos.forms import (AdicionarArquivoForm, AdicionarDisciplinaForm,
					BuscarMaterialForm, EditarDisciplinaForm, EditarArquivoForm)
from compleaks.arquivos.models import Arquivo, Disciplina
import jinja2
import datetime
import os
from zipfile import *					

arquivos = Blueprint('arquivos', __name__,template_folder='templates/arquivos')

@arquivos.route('/adicionar', methods= ['POST', 'GET'])
@login_required
def adicionar():
	form_add = AdicionarArquivoForm()

	if form_add.validate_on_submit():
		data = datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")
		disciplina = form_add.disciplina.data
		ano = int(form_add.ano.data)
		semestre = form_add.semestre.data
		tipo = form_add.tipo_conteudo.data
		professor = form_add.professor.data
		observacoes = form_add.observacoes.data
		nome = disciplina + " - " + tipo + " - " + data
		print("To aq 2")
		target = os.path.join(current_app, 'static/uploads')

		if not os.path.isdir(target):
			os.mkdir(target)
		print("To aq 3")
		file_name = target + "/" + nome + ".zip"
		zip_archive = ZipFile(file_name, "w")

		file = form_add.arquivo.data
		print("To aq 4")
		filename = file.filename
		destination = "/".join([target, filename])
		file.save(destination)
		zip_archive.write(destination, destination[len(target) + 1:])
		os.remove(destination)

		new_arq = Arquivo(arquivo=nome, disciplina_id=disciplina, ano=ano, semestre=semestre,
						 tipo_conteudo=tipo, professor_id=professor, usuario_id=current_user.id,
						  data=data)
		
		new_arq.observacoes = observacoes

		db.session.add(new_arq)
		db.session.commit()
		print("To aq 5")

		flash("Arquivo adicionado com sucesso")
	
	return render_template('adicionar_arquivo.html', form_add=form_add)

@arquivos.route('/editar/<int:arq_id>', methods=['POST', 'GET'])
def editar(arq_id):
	form = EditarArquivoForm()

	arquivo = Arquivo.query.get(arq_id)

	if current_user != arquivo.author:
		abort(403)

	if form.validate_on_submit():
		arquivo.ano = form.ano.data
		arquivo.semestre = form.semestre.data
		arquivo.tipo_conteudo = int(form.tipo_conteudo.data)
		arquivo.professor_id = form.professor.data
		arquivo.observacoes = form.observacoes.data
		arquivo.disciplina_id =form.disciplina.data

		db.session.commit()

	form.ano.data = arquivo.ano
	form.semestre.data = arquivo.semestre
	form.tipo_conteudo.data = arquivo.tipo_conteudo
	form.professor.data = arquivo.professor_id
	form.observacoes.data = arquivo.observacoes
	form.disciplina.data = arquivo.disciplina_id
	

	return render_template('editar_arquivo.html', form=form)

@arquivos.route('/listar', methods=['POST', 'GET'])
def listar():
	arquivos = Arquivo.query.order_by(Arquivo.data_submissao.desc())
	return render_template('todos_arquivos.html', arquivos=arquivos)

@arquivos.route('/buscar', methods=['POST', 'GET'])
def buscar():

	form = BuscarMaterialForm()

	if form.validate_on_submit():

		return redirect(url_for('verconsulta'))

	return render_template('buscar.html', form=form)

@arquivos.route('/excluir/<int:aqr_id>', methods=['POST', 'GET'])
def excluir(aqr_id):
	if not current_user.is_amin:
		abort(403)
	arquivo = Arquivo.query.filter_by(id=aqr_id)
	db.session.delete(arquivo)
	db.session.commit()
	return redirect(url_for('arquivos.listar'))

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