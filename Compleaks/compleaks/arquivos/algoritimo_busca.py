from flask import (render_template, Blueprint, url_for, redirect,
 					flash, current_app, request, abort)
from compleaks import db, dist
from flask_login import current_user, login_required
from compleaks.arquivos.forms import (AdicionarArquivoForm,
										BuscarMaterialForm, 
										EditarArquivoForm)
from compleaks.arquivos.models import Arquivo
from compleaks.professores.models import Professor
from compleaks.disciplinas.models import Disciplina
from compleaks.arquivos.views import arquivos
from compleaks.usuarios.forms import LoginForm

'''Tipo, preciso de filtrar a query que quero por tipode usuário e tipo de arquivo, logo, acaba que para
seguir o mesmo rumo na paginação preciso ter o estado anterior, o que causa essas grandes quantidades de
linhas é o fato	de uma query tem de ser feita na mesma instrução, ou seja não pode ser filtrada depois'''
@arquivos.route('/busca/<admin>/<int:filtro>/<pesquisa>/<tip_arquiv>', 
	methods=['POST', 'GET'])
@arquivos.route('/busca', defaults={"filtro":None,"admin":None,"pesquisa":None,
	"tip_arquiv":None}, methods=['POST', 'GET'])
def buscar(admin,filtro,pesquisa,tip_arquiv):

	form_login = LoginForm()

	form = BuscarMaterialForm()
	page = request.args.get('page', 1, type=int)

	if current_user.is_authenticated:
		if current_user.is_admin:
			arquivos = Arquivo.query.order_by(Arquivo.data_submissao.desc())\
							.paginate(page=page, per_page=12)
		else:
			arquivos = Arquivo.query.order_by(Arquivo.data_submissao.desc())\
					.filter_by(ativado=True).paginate(page=page, per_page=12)
	else:
		arquivos = Arquivo.query.order_by(Arquivo.data_submissao.desc())\
				.filter_by(ativado=True).paginate(page=page, per_page=12)
	existe_arquivo = True


	arquivos_row_1 = []
	arquivos_row_2 = []
	arquivos_row_3 = []


	navigation_data = []
	navigation_data.append(filtro)

	if current_user.is_authenticated: 
		if current_user.is_admin:
			navigation_data.append("adm")

		else:
			navigation_data.append("normal")
	else:
		navigation_data.append("normal")


	navigation_data.append(pesquisa)
	navigation_data.append(tip_arquiv)

	if current_user.is_authenticated: 
		if current_user.is_admin:

			if form.validate_on_submit():
				
				tip_arquiv = form.tipo_arquivo.data

				if tip_arquiv != 'all':

					if int(form.filtrar.data) == 1:

						pesquisa = form.disciplina.data
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
											.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.tipo_conteudo == tip_arquiv).first()
						print(existe_arquivo)
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
									.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.tipo_conteudo.like('%'+tip_arquiv+'%'))\
									.paginate(page=page, per_page=12)
					
					if int(form.filtrar.data) == 2:
						
						pesquisa = 	form.professor.data
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
											.filter(Professor.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.tipo_conteudo == tip_arquiv).first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
									.filter(Professor.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.tipo_conteudo == tip_arquiv)\
									.paginate(page=page, per_page=12)

					if int(form.filtrar.data) is 3:
						pesquisa = "False"
						existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv).first()
						arquivos = Arquivo.query\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.paginate(page=page, per_page=12)
				
				else:
					if int(form.filtrar.data) == 1:

						pesquisa = form.disciplina.data
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
											.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
											.first()
						arquivos =db.session.query(Arquivo)\
									.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
									.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
									.paginate(page=page, per_page=12)
					
					if int(form.filtrar.data) == 2:
						
						pesquisa = 	form.professor.data
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
											.filter(Professor.nome.like('%'+pesquisa+'%'))\
											.first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
									.filter(Professor.nome.like('%'+pesquisa+'%'))\
									.paginate(page=page, per_page=12)

					if int(form.filtrar.data) is 3:
						pesquisa = "False"
						existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv).first()
						arquivos = Arquivo.query\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.paginate(page=page, per_page=12)
				
				navigation_data.clear()
				navigation_data.append(int(form.filtrar.data))

				if current_user.is_authenticated: 
					if current_user.is_admin:
						navigation_data.append("adm")
				else:
					navigation_data.append("normal")
				navigation_data.append(pesquisa)
				navigation_data.append(tip_arquiv)

				contador = 0
				arquivos_row_1.clear()
				arquivos_row_2.clear()
				arquivos_row_3.clear()
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

				for row in arquivos_rows:
					for arquivo in row:
						arquivo.avaliado = False

				if current_user.is_authenticated:
					for row in arquivos_rows:
						for arquivo in row:
							for avl in arquivo.avaliacoes:
								if avl in current_user.avaliacoes:
									arquivo.avaliado = True

				total = 0.0
				for row in arquivos_rows:
					for arquivo in row:
						total = 0.0
						if len(arquivo.avaliacoes): 
							for avl in arquivo.avaliacoes:
								total = total + avl.nota
							total = total/len(arquivo.avaliacoes)
						else:
							total = 0.0
						
						arquivo.nota_decimal = round(total, 1)

				return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos,
					 	arquivos_rows=arquivos_rows, dist=dist,
					existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)

			if filtro:

				if tip_arquiv != 'all':

					if filtro == 1:

						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
											.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.tipo_conteudo == tip_arquiv).first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
									.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.tipo_conteudo == tip_arquiv)\
									.paginate(page=page, per_page=12)
					
					if filtro == 2:
						
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
											.filter(Professor.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.tipo_conteudo == tip_arquiv)\
											.first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
									.filter(Professor.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.tipo_conteudo == tip_arquiv)\
									.paginate(page=page, per_page=12)

					if filtro is 3:
						existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv).first()
						arquivos = Arquivo.query\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.paginate(page=page, per_page=12)
				
				else:
					if filtro == 1:

						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
											.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
											.first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
									.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
									.paginate(page=page, per_page=12)
					
					if filtro == 2:
						
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
											.filter(Professor.nome.like('%'+pesquisa+'%'))\
											.first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
									.filter(Professor.nome.like('%'+pesquisa+'%'))\
									.paginate(page=page, per_page=12)

					if filtro is 3:
						existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv).first()
						arquivos = Arquivo.query\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.paginate(page=page, per_page=12)


				contador = 0
				arquivos_row_1.clear()
				arquivos_row_2.clear()
				arquivos_row_3.clear()
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

				for row in arquivos_rows:
					for arquivo in row:
						arquivo.avaliado = False

				if current_user.is_authenticated:
					for row in arquivos_rows:
						for arquivo in row:
							for avl in arquivo.avaliacoes:
								if avl in current_user.avaliacoes:
									arquivo.avaliado = True

				total = 0.0
				for row in arquivos_rows:
					for arquivo in row:
						total = 0.0
						if len(arquivo.avaliacoes): 
							for avl in arquivo.avaliacoes:
								total = total + avl.nota
							total = total/len(arquivo.avaliacoes)
						else:
							total = 0.0
						arquivo.nota_decimal = round(total, 1)

				return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos, 
					 	arquivos_rows=arquivos_rows, form_login=form_login, dist=dist,
					existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)	

		else:

			if form.validate_on_submit():
				
				tip_arquiv = form.tipo_arquivo.data

				if tip_arquiv != 'all':

					if int(form.filtrar.data) == 1:

						pesquisa = form.disciplina.data
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
											.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.tipo_conteudo == tip_arquiv)\
											.filter(Arquivo.ativado == True).first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
									.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.tipo_conteudo == tip_arquiv)\
									.filter(Arquivo.ativado == True)\
									.paginate(page=page, per_page=12)
					
					if int(form.filtrar.data) == 2:
						
						pesquisa = 	form.professor.data
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
											.filter(Professor.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.tipo_conteudo == tip_arquiv)\
											.filter(Arquivo.ativado == True).first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
									.filter(Professor.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.tipo_conteudo == tip_arquiv)\
									.filter(Arquivo.ativado == True)\
									.paginate(page=page, per_page=12)

					if int(form.filtrar.data) is 3:
						pesquisa = "False"
						existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
											.filter_by(ativado=True).first()
						arquivos = Arquivo.query.filter_by(ativado=True)\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.paginate(page=page, per_page=12)
				
				else:
					if int(form.filtrar.data) == 1:

						pesquisa = form.disciplina.data
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
											.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.ativado == True).first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
									.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.ativado == True)\
									.paginate(page=page, per_page=12)
					
					if int(form.filtrar.data) == 2:
						
						pesquisa = 	form.professor.data
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
											.filter(Professor.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.ativado == True).first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
									.filter(Professor.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.ativado == True)\
									.paginate(page=page, per_page=12)

					if int(form.filtrar.data) is 3:
						pesquisa = "False"
						existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
											.filter_by(ativado=True).first()
						arquivos = Arquivo.query.filter_by(ativado=True)\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.paginate(page=page, per_page=12)
				
				navigation_data.clear()
				navigation_data.append(int(form.filtrar.data))
				if current_user.is_authenticated: 
					if current_user.is_admin:
						navigation_data.append("adm")
					else:
						navigation_data.append("normal")
				else:
					navigation_data.append("normal")
				navigation_data.append(pesquisa)
				navigation_data.append(tip_arquiv)


				contador = 0
				arquivos_row_1.clear()
				arquivos_row_2.clear()
				arquivos_row_3.clear()
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

				for row in arquivos_rows:
					for arquivo in row:
						arquivo.avaliado = False

				if current_user.is_authenticated:
					for row in arquivos_rows:
						for arquivo in row:
							for avl in arquivo.avaliacoes:
								if avl in current_user.avaliacoes:
									arquivo.avaliado = True

				total = 0.0
				for row in arquivos_rows:
					for arquivo in row:
						total = 0.0
						if len(arquivo.avaliacoes): 
							for avl in arquivo.avaliacoes:
								total = total + avl.nota
							total = total/len(arquivo.avaliacoes)
						else:
							total = 0.0

						arquivo.nota_decimal = round(total, 1)

				return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos, 
					 	arquivos_rows=arquivos_rows, form_login=form_login, dist=dist,
					existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)

			if filtro:

				if tip_arquiv != 'all':

					if filtro == 1:

						existe_arquivo =  db.session.query(Arquivo)\
											.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
											.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
											.filter_by(tipo_conteudo=tip_arquiv)\
											.filter(Arquivo.ativado == True).first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
									.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.filter(Arquivo.ativado == True)\
									.paginate(page=page, per_page=12)
					
					if filtro == 2:
						
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
											.filter(Professor.nome.like('%'+pesquisa+'%'))\
											.filter_by(tipo_conteudo=tip_arquiv)\
											.filter(Arquivo.ativado == True).first()
						arquivos = Arquivo.query.filter_by(ativado=True)\
									.filter(Arquivo.professor.nome.contains(pesquisa))\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.paginate(page=page, per_page=12)

					if filtro is 3:
						existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
										.filter_by(ativado=True).first()
						arquivos = Arquivo.query.filter_by(ativado=True)\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.paginate(page=page, per_page=12)
				
				else:
					if filtro == 1:

						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
											.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.ativado == True).first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
									.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.ativado == True)\
									.paginate(page=page, per_page=12)
					
					if filtro == 2:
						
						existe_arquivo = db.session.query(Arquivo)\
											.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
											.filter(Professor.nome.like('%'+pesquisa+'%'))\
											.filter(Arquivo.ativado == True).first()
						arquivos = db.session.query(Arquivo)\
									.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
									.filter(Professor.nome.like('%'+pesquisa+'%'))\
									.filter(Arquivo.ativado == True)\
									.paginate(page=page, per_page=12)

					if filtro is 3:
						existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
										.filter_by(ativado=True).first()
						arquivos = Arquivo.query.filter_by(ativado=True)\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.paginate(page=page, per_page=12)

				contador = 0
				arquivos_row_1.clear()
				arquivos_row_2.clear()
				arquivos_row_3.clear()
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

				for row in arquivos_rows:
					for arquivo in row:
						arquivo.avaliado = False

				if current_user.is_authenticated:
					for row in arquivos_rows:
						for arquivo in row:
							for avl in arquivo.avaliacoes:
								if avl in current_user.avaliacoes:
									arquivo.avaliado = True

				total = 0.0
				for row in arquivos_rows:
					for arquivo in row:
						total = 0.0
						if len(arquivo.avaliacoes): 
							for avl in arquivo.avaliacoes:
								total = total + avl.nota
							total = total/len(arquivo.avaliacoes)
						else:
							total = 0.0

						arquivo.nota_decimal = round(total, 1)

				return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos, 
					 	arquivos_rows=arquivos_rows, form_login=form_login, dist=dist,
					existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)	

	else:

		if form.validate_on_submit():
			
			tip_arquiv = form.tipo_arquivo.data

			if tip_arquiv != 'all':

				if int(form.filtrar.data) == 1:

					pesquisa = form.disciplina.data
					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
										.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.tipo_conteudo == tip_arquiv)\
										.filter(Arquivo.ativado == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
								.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
								.filter(Arquivo.tipo_conteudo == tip_arquiv)\
								.filter(Arquivo.ativado == True)\
								.paginate(page=page, per_page=12)
				
				if int(form.filtrar.data) == 2:
					
					pesquisa = 	form.professor.data
					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
										.filter(Professor.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.tipo_conteudo == tip_arquiv)\
										.filter(Arquivo.ativado == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
								.filter(Professor.nome.like('%'+pesquisa+'%'))\
								.filter(Arquivo.tipo_conteudo == tip_arquiv)\
								.filter(Arquivo.ativado == True)\
								.paginate(page=page, per_page=12)

				if int(form.filtrar.data) is 3:
					pesquisa = "False"
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
										.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)
			
			else:
				if int(form.filtrar.data) == 1:

					pesquisa = form.disciplina.data
					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
										.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.ativado == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
								.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
								.filter(Arquivo.ativado == True)\
								.paginate(page=page, per_page=12)
				
				if int(form.filtrar.data) == 2:
					
					pesquisa = 	form.professor.data
					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
										.filter(Professor.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.ativado == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
								.filter(Professor.nome.like('%'+pesquisa+'%'))\
								.filter(Arquivo.ativado == True)\
								.paginate(page=page, per_page=12)

				if int(form.filtrar.data) is 3:
					pesquisa = "False"
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
										.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)
			
			navigation_data.clear()
			navigation_data.append(int(form.filtrar.data))
			if current_user.is_authenticated: 
				if current_user.is_admin:
					navigation_data.append("adm")
				else:
					navigation_data.append("normal")
			else:
				navigation_data.append("normal")
			navigation_data.append(pesquisa)
			navigation_data.append(tip_arquiv)


			contador = 0
			arquivos_row_1.clear()
			arquivos_row_2.clear()
			arquivos_row_3.clear()
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

			for row in arquivos_rows:
				for arquivo in row:
					arquivo.avaliado = False

			if current_user.is_authenticated:
				for row in arquivos_rows:
					for arquivo in row:
						for avl in arquivo.avaliacoes:
							if avl in current_user.avaliacoes:
								arquivo.avaliado = True

			total = 0.0
			for row in arquivos_rows:
				for arquivo in row:
					total = 0.0
					if len(arquivo.avaliacoes): 
						for avl in arquivo.avaliacoes:
							total = total + avl.nota
						total = total/len(arquivo.avaliacoes)
					else:
						total = 0.0

					arquivo.nota_decimal = round(total, 1)


			return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos, 
				 	arquivos_rows=arquivos_rows, form_login=form_login, dist=dist,
				existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)

		if filtro:

			if tip_arquiv != 'all':

				if filtro == 1:

					existe_arquivo =  db.session.query(Arquivo)\
										.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
										.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
										.filter_by(tipo_conteudo=tip_arquiv)\
										.filter(Arquivo.ativado == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
								.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.filter(Arquivo.ativado == True)\
								.paginate(page=page, per_page=12)
				
				if filtro == 2:
					
					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
										.filter(Professor.nome.like('%'+pesquisa+'%'))\
										.filter_by(tipo_conteudo=tip_arquiv)\
										.filter(Arquivo.ativado == True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter(Arquivo.professor.nome.contains(pesquisa))\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)

				if filtro is 3:
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
									.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)
			
			else:
				if filtro == 1:

					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
										.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.ativado == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
								.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
								.filter(Arquivo.ativado == True)\
								.paginate(page=page, per_page=12)
				
				if filtro == 2:
					
					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
										.filter(Professor.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.ativado == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
								.filter(Professor.nome.like('%'+pesquisa+'%'))\
								.filter(Arquivo.ativado == True)\
								.paginate(page=page, per_page=12)

				if filtro is 3:
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
									.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)

			contador = 0
			arquivos_row_1.clear()
			arquivos_row_2.clear()
			arquivos_row_3.clear()
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

			for row in arquivos_rows:
				for arquivo in row:
					arquivo.avaliado = False

			if current_user.is_authenticated:
				for row in arquivos_rows:
					for arquivo in row:
						for avl in arquivo.avaliacoes:
							if avl in current_user.avaliacoes:
								arquivo.avaliado = True
			total = 0.0
			for row in arquivos_rows:
				for arquivo in row:
					total = 0.0
					for avl in arquivo.avaliacoes:
						total = total + avl.nota
					total = total/len(arquivo.avaliacoes)
					arquivo.nota_decimal = round(total, 1)

			return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos, 
				 	arquivos_rows=arquivos_rows, form_login=form_login, dist=dist,
				existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)
	
	contador = 0
	arquivos_row_1.clear()
	arquivos_row_2.clear()
	arquivos_row_3.clear()
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

	for row in arquivos_rows:
		for arquivo in row:
			arquivo.avaliado = False

	if current_user.is_authenticated:
		for row in arquivos_rows:
			for arquivo in row:
				for avl in arquivo.avaliacoes:
					if avl in current_user.avaliacoes:
						arquivo.avaliado = True


	total = 0.0
	for row in arquivos_rows:
		for arquivo in row:
			total = 0.0
			if len(arquivo.avaliacoes): 
				for avl in arquivo.avaliacoes:
					total = total + avl.nota
				total = total/len(arquivo.avaliacoes)
			else:
				total = 0.0

			arquivo.nota_decimal = round(total, 1)



	return render_template('buscar_arq.html', tip_arquiv="all", arquivos=arquivos ,
			arquivos_rows=arquivos_rows, form_login=form_login, dist=dist,
		existe_arquivo=existe_arquivo, navigation_data=navigation_data,form=form)



	'''
	else:

		if form.validate_on_submit():
				
			tip_arquiv = form.tipo_arquivo.data

			if tip_arquiv != 'all':

				if int(form.filtrar.data) == 1:

					pesquisa = form.disciplina.data
					existe_arquivo = Arquivo.query.filter_by(ativado=True)\
									.filter(Arquivo.disciplina.nome\
									.contains(pesquisa))\
									.filter_by(tipo_conteudo=tip_arquiv).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter(Arquivo.disciplina.nome\
								.contains(pesquisa))\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)
				
				if int(form.filtrar.data) == 2:
					
					pesquisa = 	form.professor.data
					existe_arquivo = Arquivo.query.filter(Arquivo.professor.nome.contains(pesquisa))\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter(Arquivo.professor.nome.contains(pesquisa))\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)

				if int(form.filtrar.data) is 3:
					pesquisa = "False"
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
										.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)
			
			else:
				if int(form.filtrar.data) == 1:

					pesquisa = form.disciplina.data
					existe_arquivo = Arquivo.query.filter_by(ativado=True)\
									.filter(Arquivo.disciplina.nome\
									.contains(pesquisa))\
									.first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter(Arquivo.disciplina.nome\
								.contains(pesquisa))\
								.paginate(page=page, per_page=12)
				
				if int(form.filtrar.data) == 2:
					
					pesquisa = 	form.professor.data
					existe_arquivo = Arquivo.query.filter(Arquivo.professor.nome.contains(pesquisa))\
									.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter(Arquivo.professor.nome.contains(pesquisa))\
								.paginate(page=page, per_page=12)

				if int(form.filtrar.data) is 3:
					pesquisa = "False"
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
									.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)
			
			navigation_data.clear()
			navigation_data.append(int(form.filtrar.data))
			if current_user.is_authenticated: 
				if current_user.is_admin:
					navigation_data.append("adm")
			else:
				navigation_data.append("normal")
			navigation_data.append(pesquisa)
			navigation_data.append(tip_arquiv)


			contador = 0
			arquivos_row_1.clear()
			arquivos_row_2.clear()
			arquivos_row_3.clear()
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

			return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos, 
					 	arquivos_rows=arquivos_rows, form_login=form_login,
				existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)

		if filtro:

			if tip_arquiv != 'all':

				if filtro == 1:

					existe_arquivo = Arquivo.query.filter_by(ativado=True)\
									.filter(Arquivo.disciplina.nome\
									.contains(pesquisa))\
									.filter_by(tipo_conteudo=tip_arquiv).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter(Arquivo.disciplina.nome\
								.contains(pesquisa))\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)
				
				if filtro == 2:
					
					existe_arquivo = Arquivo.query.filter(Arquivo.professor.nome.contains(pesquisa))\
									.filter_by(tipo_conteudo=tip_arquiv)\
									.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter(Arquivo.professor.nome.contains(pesquisa))\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)

				if filtro is 3:
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
									.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)
			
			else:
				if filtro == 1:

					existe_arquivo = Arquivo.query.filter_by(ativado=True)\
									.filter(Arquivo.disciplina.nome\
									.contains(pesquisa))\
									.first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter(Arquivo.disciplina.nome\
								.contains(pesquisa))\
								.paginate(page=page, per_page=12)
				
				if filtro == 2:
					
					existe_arquivo = Arquivo.query.filter(Arquivo.professor.nome.contains(pesquisa))\
									.filter_by(ativado=True).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter(Arquivo.professor.nome.contains(pesquisa))\
								.paginate(page=page, per_page=12)

				if filtro is 3:
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv).first()
					arquivos = Arquivo.query.filter_by(ativado=True)\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)

			contador = 0
			arquivos_row_1.clear()
			arquivos_row_2.clear()
			arquivos_row_3.clear()
			for arquivo in arquivos.items:
				arquivos_row_1.append(arquivo)
				if contador >= 4:
					break 
				contador = contador + 1

			contador = 0
			for arquivo in arquivos.items:
				if contador >= 4:
					arquivos_row_2.append(arquivo)
				if contador >= 8:
					break
				contador = contador + 1				

			contador = 0
			for arquivo in arquivos.items:
				if contador >= 8:
					arquivos_row_3.append(arquivo)
				if contador >= 12:
					break
				contador = contador + 1	
			
			arquivos_rows = [arquivos_row_1, arquivos_row_2, arquivos_row_3]

			return render_template('buscar_arq.html',tip_arquiv=tip_arquiv, arquivos=arquivos, 
					 	arquivos_rows=arquivos_rows, form_login=form_login,
				existe_arquivo=existe_arquivo, navigation_data=navigation_data, form=form)			
	
	'''
