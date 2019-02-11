from flask import (render_template, Blueprint, url_for, redirect,
 					flash, current_app, request, abort)
from compleaks import db
from flask_login import current_user, login_required
from compleaks.arquivos.forms import (AdicionarArquivoForm,
										BuscarMaterialForm, 
										EditarArquivoForm)
from compleaks.arquivos.models import Arquivo
from compleaks.professores.models import Professor
from compleaks.disciplinas.models import Disciplina
from compleaks.usuarios.forms import LoginForm
import jinja2
import datetime
import os
from zipfile import ZipFile
from datetime import datetime				

arquivos = Blueprint('arquivos', __name__,template_folder='templates/arquivos')

from compleaks.arquivos.algoritimo_busca import buscar

@arquivos.route('/adicionar', methods= ['POST', 'GET'])
@login_required
def adicionar():
	form_add = AdicionarArquivoForm()

	professores = Professor.query.filter_by(is_eligible=True)
	disciplinas = Disciplina.query.filter_by(is_eligible=True)

	if form_add.validate_on_submit():
		data = datetime.now()

		if request.method == 'POST':

			disciplina = request.form.get("disciplina")
			professor = request.form.get("professor")

		try:
			disciplina = (int(disciplina))
		except:
			form_add = AdicionarArquivoForm()
			flash("Não foi possivel realizar a operação! Favor tente novamente", "danger")
			return render_template('adicionar_arquivo.html',professores=professores, 
									disciplinas=disciplinas, form_add=form_add)

		if not disciplina:
			form_add = AdicionarArquivoForm()
			flash("Não foi possivel realizar a operação! Favor tente novamente", "danger")
			return render_template('adicionar_arquivo.html',professores=professores, 
									disciplinas=disciplinas, form_add=form_add)		
			
		try:
			professor = (int(professor))
		except:
			professor = 0

		page = request.args.get('page', 1, type=int)
			
		ano = int(form_add.ano.data)
		semestre = form_add.semestre.data
		tipo = form_add.tipo_conteudo.data
		observacoes = form_add.observacoes.data

		nome = str(disciplina) + " - " + tipo + " - " + str(data.strftime('%d - %m - %y'))
		target = os.path.join(current_app.root_path, 'static/uploads')

		file_name = target + "/" + nome + ".zip"

		file = form_add.arquivo.data
		filename = file.filename
		extensao = filename.split('.')[-1]
		destination = "/".join([target, filename])
		file.save(destination)

		zip_archive = ZipFile(file_name, "w")
		zip_archive.write(destination, destination[len(target) + 1:])
		os.remove(destination)

		new_arq = Arquivo(arquivo=nome, disciplina_id=disciplina, ano=ano, semestre=semestre,
						 tipo_conteudo=tipo, professor_id=professor, 
						 usuario_id=current_user.id, extensao=extensao)
		
		new_arq.observacoes = observacoes

		db.session.add(new_arq)
		db.session.commit()

		flash("Nossa comunidade agradece a sua contribuição.", "success")
	
	return render_template('adicionar_arquivo.html',professores=professores, 
									disciplinas=disciplinas, form_add=form_add)

@arquivos.route('/editar/<int:arq_id>', methods=['POST', 'GET'])
@login_required
def editar(arq_id):
	form = EditarArquivoForm()

	professores = Professor.query.filter_by(is_eligible=True)
	disciplinas = Disciplina.query.filter_by(is_eligible=True)

	arquivo = Arquivo.query.get_or_404(arq_id)

	if current_user != arquivo.author or not arquivo.is_eligible:
		abort(403)

	if form.validate_on_submit() and arquivo.is_eligible:

		if request.method == 'POST':

			disciplina = request.form.get("disciplina")
			professor = request.form.get("professor")

		try:
			disciplina = (int(disciplina))
		except ValueError as e:
			form = EditarArquivoForm()
			flash("Não foi possivel realizar a operação!", "danger")
			return redirect(url_for('arquivos.buscar'))

		except NameError as e:
			form = EditarArquivoForm()
			flash("Não foi possivel realizar a operação! Favor tente novamente", "danger")
			return redirect(url_for('arquivos.buscar'))

		if not disciplina:
			form = EditarArquivoForm()
			flash("Não foi possivel realizar a operação!", "danger")
			return redirect(url_for('arquivos.buscar'))	
			
		try:
			professor = (int(professor))
		except:
			professor = 0

		arquivo.ano = form.ano.data
		arquivo.semestre = form.semestre.data
		arquivo.tipo_conteudo = int(form.tipo_conteudo.data)
		arquivo.professor_id = professor
		arquivo.observacoes = form.observacoes.data
		arquivo.disciplina_id = disciplina

		db.session.commit()

		flash("Nossa comunidade agradece a sua contribuição.", "success")

	form.ano.data = arquivo.ano
	form.semestre.data = arquivo.semestre
	form.tipo_conteudo.data = arquivo.tipo_conteudo
	professor_selecionado = arquivo.professor_id
	form.observacoes.data = arquivo.observacoes
	disciplina_selecionada = arquivo.disciplina_id
	
	return render_template('editar_arquivo.html',professores=professores, 
									disciplinas=disciplinas, prof_selecionado=professor_selecionado,
									disc_selecionada=disciplina_selecionada, form=form)

@arquivos.route('/listar', methods=['POST', 'GET'])
def listar():

	form_login = LoginForm()
	page = request.args.get('page', 1, type=int)
	arquivos = Arquivo.query.filter_by(is_eligible=True)\
				.order_by(Arquivo.data_submissao.desc())\
				.paginate(page=page, per_page=12)
	tem_arquivo = Arquivo.query.order_by(Arquivo.data_submissao.desc()).first()
	if tem_arquivo is None:
		abort(404)
	
	try:
		if current_user.is_admin:
			arquivos = Arquivo.query\
					.order_by(Arquivo.data_submissao.desc())\
					.paginate(page=page, per_page=12)
			return render_template('todos_arquivos_adm.html', arquivos=arquivos, form_login=form_login)
		else:
			return render_template('todos_arquivos_normal.html', arquivos=arquivos, form_login=form_login)

	except:
		return render_template('todos_arquivos_normal.html', arquivos=arquivos, form_login=form_login)



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
	flash("Arquivo excluído com sucesso.", "success")
	return redirect(url_for('arquivos.buscar'))

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
	flash("O arquivo foi restaurado com sucesso.", "success")
	return redirect(url_for('arquivos.buscar'))


@arquivos.route('/deletados', methods=['GET', "POST"])
def deletados():
	if not current_user.is_admin:
		abort(404)

	page = request.args.get('page', 1, type=int)	
	arquivos = Arquivo.query.filter_by(is_eligible=False).paginate(page=page, per_page=12)

	arquivos_row_1 = []
	arquivos_row_2 = []
	arquivos_row_3 = []
	contador = 0
	for arquivo in arquivos.items:
		if contador >= 4:
			break 
		arquivos_row_1.append(arquivo)
		contador = contador + 1

	contador = 0
	for arquivo in arquivos.items:
		if contador >= 8:
			break
		if contador >= 4:
			arquivos_row_2.append(arquivo)
		contador = contador + 1				

	contador = 0
	for arquivo in arquivos.items:
		if contador >= 12:
			break
		if contador >= 8:
			arquivos_row_3.append(arquivo)
		contador = contador + 1				

	arquivos_rows = [arquivos_row_1, arquivos_row_2, arquivos_row_3]


	return render_template('arquivos_deletados.html', arquivos=arquivos, arquivos_rows=arquivos_rows)