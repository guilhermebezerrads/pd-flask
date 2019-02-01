from flask import render_template, Blueprint, url_for, redirect, flash, current_app, request
from compleaks import db
from flask_login import current_user, login_required
from compleaks.arquivos.forms import (AdicionarArquivoForm, AdicionarDisciplinaForm,
					BuscarMaterialForm, EditarDisciplinaForm, EditarArquivoForm)
from compleaks.arquivos.models import Arquivo, Disciplina
import jinja2
import datetime
import os
from zipfile import ZipFile
from datetime import datetime				

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
		target = os.path.join(current_app.root_path, 'static/uploads')

		file_name = target + "/" + nome + ".zip"

		file = form_add.arquivo.data
		filename = file.filename
		destination = "/".join([target, filename])
		file.save(destination)

		zip_archive = ZipFile(file_name, "w")
		zip_archive.write(destination, destination[len(target) + 1:])
		os.remove(destination)

		new_arq = Arquivo(arquivo=nome, disciplina_id=disciplina, ano=ano, semestre=semestre,
						 tipo_conteudo=tipo, professor_id=professor, usuario_id=current_user.id)
		
		new_arq.observacoes = observacoes

		db.session.add(new_arq)
		db.session.commit()

		flash("Obrigado por contribuir para a nossa comunidade maravilhosa!")
	
	return render_template('adicionar_arquivo.html', form_add=form_add)

@arquivos.route('/editar/<int:arq_id>', methods=['POST', 'GET'])
@login_required
def editar(arq_id):
	form = EditarArquivoForm()

	arquivo = Arquivo.query.get(arq_id)

	if current_user != arquivo.author or not arquivo.is_eligible:
		abort(403)

	if form.validate_on_submit() and arquivo.is_eligible:
		arquivo.ano = form.ano.data
		arquivo.semestre = form.semestre.data
		arquivo.tipo_conteudo = int(form.tipo_conteudo.data)
		arquivo.professor_id = form.professor.data
		arquivo.observacoes = form.observacoes.data
		arquivo.disciplina_id =form.disciplina.data

		db.session.commit()

		flash("Obrigado por contribuir para a nossa comunidade maravilhosa!")

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
	return render_template('todos_arquivos.html', arquivos=arquivos, arquivos_deletado=arquivos_deletado)

@arquivos.route('/buscar', methods=['POST', 'GET'])
def buscar():

	form = BuscarMaterialForm()

	if form.validate_on_submit():

		return redirect(url_for('arquivos.buscar'))

	return render_template('buscar.html', form=form)

@arquivos.route('/excluir/<int:arq_id>', methods=['POST', 'GET'])
def excluir(arq_id):
	if not current_user.is_amin:
		abort(403)
	arquivo = Arquivo.query.filter_by(id=aqr_id)
	arquivo.is_eligible = False
	arquivo.id_deletor = current_user.id
	arquivo.data_deletado = datetime.utcnow

	if request.method == "POST":
		try:
			arquivo.motivo_delete = request.form.get("motivo"+str(arquivo.id))
		except Exception as e:
			flash("Aqui não tem bobo não porra!")
			print(e)#pretendo mandar um email avisando que alguem tentou uma violação
			abort(403)
	
	db.session.commit()
	flash("Arquivo excluido com sucesso!")
	return redirect(url_for('arquivos.listar'))

@arquivos.route('/ver-consulta')
def ver_consulta():
    return render_template('ver_consulta.html')