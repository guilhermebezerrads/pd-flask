from flask import (render_template, Blueprint, url_for, redirect,
 					flash, current_app, request, abort)
from compleaks import db
from flask_login import current_user, login_required
from compleaks.arquivos.forms import (AdicionarArquivoForm,
										BuscarMaterialForm, 
										EditarArquivoForm)
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
		data = datetime.now()
		disciplina = form_add.disciplina.data
		ano = int(form_add.ano.data)
		semestre = form_add.semestre.data
		tipo = form_add.tipo_conteudo.data
		professor = form_add.professor.data
		observacoes = form_add.observacoes.data
		nome = disciplina + " - " + tipo + " - " + str(data.strftime('%d - %m - %y, %H-%M-%S'))
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

	arquivo = Arquivo.query.get_or_404(arq_id)

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
	page = request.args.get('page', 1, type=int)
	arquivos = Arquivo.query.filter_by(is_eligible=True)\
				.order_by(Arquivo.data_submissao.desc())\
				.paginate(page=page, per_page=5)
	tem_arquivo = Arquivo.query.order_by(Arquivo.data_submissao.desc()).first()
	if tem_arquivo is None:
		abort(404)
	
	if current_user.is_admin:
		arquivos = Arquivo.query\
				.order_by(Arquivo.data_submissao.desc())\
				.paginate(page=page, per_page=5)
		return render_template('todos_arquivos_adm.html', arquivos=arquivos)
	else:
		return render_template('todos_arquivos_normal.html', arquivos=arquivos)

@arquivos.route('/busca/<admin>/<int:filtro>/<pesquisa>/<tip_arquiv>', methods=['POST', 'GET'])
@arquivos.route('/busca',defaults={"filtro":None,"admin":None,"pesquisa":None,"tip_arquiv":None}, methods=['POST', 'GET'])
def buscar(admin,filtro,pesquisa,tip_arquiv):

	form = BuscarMaterialForm()
	page = request.args.get('page', 1, type=int)
	arquivos = Arquivo.query.order_by(Arquivo.data_submissao.desc())\
				.paginate(page=page, per_page=5)
	existe_arquivo = True
	navigation_data = []
	navigation_data.append(filtro)
	if current_user.is_admin:
		navigation_data.append("adm")
	else:
		navigation_data.append("normal")

	navigation_data.append(pesquisa)
	navigation_data.append(tip_arquiv)

	if form.validate_on_submit():
		
		tip_arquiv = form.tipo_arquivo.data

		if tip_arquiv != 'all':

			if int(form.filtrar.data) == 1:

				pesquisa = form.disciplina.data
				existe_arquivo = Arquivo.query\
								.filter(Arquivo.disciplina_id\
								.contains(int(pesquisa)))\
								.filter_by(tipo_conteudo=tip_arquiv).first()
				arquivos = Arquivo.query\
							.filter(Arquivo.disciplina_id\
							.contains(int(pesquisa)))\
							.filter_by(tipo_conteudo=tip_arquiv)\
							.paginate(page=page, per_page=5)
			
			if int(form.filtrar.data) == 2:
				
				pesquisa = 	form.professor.data
				existe_arquivo = Arquivo.query.filter_by(professor_id=int(pesquisa))\
								.filter_by(tipo_conteudo=tip_arquiv).first()
				arquivos = Arquivo.query\
							.filter_by(professor_id=int(pesquisa))\
							.filter_by(tipo_conteudo=tip_arquiv)\
							.paginate(page=page, per_page=5)

			if int(form.filtrar.data) is 3:
				pesquisa = "False"
				existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv).first()
				arquivos = Arquivo.query\
							.filter_by(tipo_conteudo=tip_arquiv)\
							.paginate(page=page, per_page=5)
		
		else:
			if int(form.filtrar.data) == 1:

				pesquisa = form.disciplina.data
				existe_arquivo = Arquivo.query\
								.filter(Arquivo.disciplina_id\
								.contains(int(pesquisa)))\
								.first()
				arquivos = Arquivo.query\
							.filter(Arquivo.disciplina_id\
							.contains(int(pesquisa)))\
							.paginate(page=page, per_page=5)
			
			if int(form.filtrar.data) == 2:
				
				pesquisa = 	form.professor.data
				existe_arquivo = Arquivo.query.filter_by(professor_id=int(pesquisa))\
								.first()
				arquivos = Arquivo.query\
							.filter_by(professor_id=int(pesquisa))\
							.paginate(page=page, per_page=5)

			if int(form.filtrar.data) is 3:
				pesquisa = "False"
				existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv).first()
				arquivos = Arquivo.query\
							.filter_by(tipo_conteudo=tip_arquiv)\
							.paginate(page=page, per_page=5)
		
		navigation_data.clear()
		navigation_data.append(int(form.filtrar.data))
		if current_user.is_admin:
			navigation_data.append("adm")
		else:
			navigation_data.append("normal")
		navigation_data.append(pesquisa)
		navigation_data.append(tip_arquiv)

		return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos, existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)

	if filtro:

		if tip_arquiv != 'all':

			if filtro == 1:

				existe_arquivo = Arquivo.query\
								.filter(Arquivo.disciplina_id\
								.contains(int(pesquisa)))\
								.filter_by(tipo_conteudo=tip_arquiv).first()
				arquivos = Arquivo.query\
							.filter(Arquivo.disciplina_id\
							.contains(int(pesquisa)))\
							.filter_by(tipo_conteudo=tip_arquiv)\
							.paginate(page=page, per_page=5)
			
			if filtro == 2:
				
				existe_arquivo = Arquivo.query.filter_by(professor_id=int(pesquisa))\
								.filter_by(tipo_conteudo=tip_arquiv).first()
				arquivos = Arquivo.query\
							.filter_by(professor_id=int(pesquisa))\
							.filter_by(tipo_conteudo=tip_arquiv)\
							.paginate(page=page, per_page=5)

			if filtro is 3:
				existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv).first()
				arquivos = Arquivo.query\
							.filter_by(tipo_conteudo=tip_arquiv)\
							.paginate(page=page, per_page=5)
		
		else:
			print("To aqui¹")
			if filtro == 1:

				existe_arquivo = Arquivo.query\
								.filter(Arquivo.disciplina_id\
								.contains(int(pesquisa)))\
								.first()
				arquivos = Arquivo.query\
							.filter(Arquivo.disciplina_id\
							.contains(int(pesquisa)))\
							.paginate(page=page, per_page=5)
			
			if filtro == 2:
				
				existe_arquivo = Arquivo.query.filter_by(professor_id=int(pesquisa))\
								.first()
				arquivos = Arquivo.query\
							.filter_by(professor_id=int(pesquisa))\
							.paginate(page=page, per_page=5)

			if filtro is 3:
				existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv).first()
				arquivos = Arquivo.query\
							.filter_by(tipo_conteudo=tip_arquiv)\
							.paginate(page=page, per_page=5)

		return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos, existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)		

	return render_template('buscar_arq.html', tip_arquiv="all", arquivos=arquivos ,existe_arquivo=existe_arquivo, navigation_data=navigation_data,form=form)

@arquivos.route('/excluir/<int:arq_id>', methods=['POST', 'GET'])
@login_required
def excluir(arq_id):
	if not current_user.is_admin:
		abort(403)
	arquivo = Arquivo.query.get_or_404(arq_id)
	arquivo.is_eligible = False
	arquivo.id_deletor = current_user.id
	arquivo.data_deletado = datetime.now()
	
	db.session.commit()
	flash("Arquivo excluido com sucesso!")
	return redirect(url_for('arquivos.listar'))

@arquivos.route('/redefinir/<int:arq_id>', methods=['POST', 'GET'])
@login_required
def redefinir(arq_id):
	if not current_user.is_admin:
		abort(403)

	arquivo = Arquivo.query.get_or_404(arq_id)
	arquivo.is_eligible = True
	arquivo.data_deletado = None
	arquivo.id_deletor = None
		
	db.session.commit()
	flash("Usuário acabou de ser redefinido ao sistema!")
	return redirect(url_for('arquivos.listar'))
