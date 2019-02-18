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
from compleaks.arquivos.views import arquivos
from compleaks.usuarios.forms import LoginForm

@arquivos.route('/busca_asn/<admin>/<int:filtro>/<pesquisa>/<tip_arquiv>', 
	methods=['POST', 'GET'])
@arquivos.route('/busca_asn/<admin>/<int:filtro>/<tip_arquiv>', 
	methods=['POST', 'GET'], defaults={"pesquisa":None})
def busca_asn(admin,filtro,pesquisa,tip_arquiv):

	print("To_aq")

	page = request.args.get('page', 1, type=int)

	if current_user.is_authenticated:
		if current_user.is_admin:
			arquivos = Arquivo.query.order_by(Arquivo.data_submissao.desc())\
							.paginate(page=page, per_page=12)
		else:
			arquivos = Arquivo.query.order_by(Arquivo.data_submissao.desc())\
					.filter_by(is_eligible=True).paginate(page=page, per_page=12)
	else:
		arquivos = Arquivo.query.order_by(Arquivo.data_submissao.desc())\
				.filter_by(is_eligible=True).paginate(page=page, per_page=12)
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

	if not pesquisa:
		navigation_data.clear()
		navigation_data.append(None)
		if current_user.is_authenticated: 
			if current_user.is_admin:
				navigation_data.append("adm")

			else:
				navigation_data.append("normal")
		else:
			navigation_data.append("normal")
		navigation_data.append(None)
		navigation_data.append(None)

	if pesquisa:
		if current_user.is_authenticated: 
			if current_user.is_admin:

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

					return render_template('busca_assincrona_adm.html',tip_arquiv=tip_arquiv, arquivos=arquivos, 
						 	arquivos_rows=arquivos_rows, 
						existe_arquivo=existe_arquivo, navigation_data=navigation_data)

		if filtro:

			if tip_arquiv != 'all':

				if filtro == 1:

					existe_arquivo =  db.session.query(Arquivo)\
										.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
										.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.tipo_conteudo==tip_arquiv)\
										.filter(Arquivo.is_eligible == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
								.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
								.filter(Arquivo.tipo_conteudo==tip_arquiv)\
								.filter(Arquivo.is_eligible == True)\
								.paginate(page=page, per_page=12)
				
				if filtro == 2:
					
					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
										.filter(Professor.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.tipo_conteudo==tip_arquiv)\
										.filter(Arquivo.is_eligible == True).first()
					arquivos = Arquivo.query.filter_by(is_eligible=True)\
								.filter(Arquivo.professor.nome.contains(pesquisa))\
								.filter(Arquivo.tipo_conteudo==tip_arquiv)\
								.paginate(page=page, per_page=12)

				if filtro is 3:
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
									.filter_by(is_eligible=True).first()
					arquivos = Arquivo.query.filter_by(is_eligible=True)\
								.filter_by(tipo_conteudo=tip_arquiv)\
								.paginate(page=page, per_page=12)
			
			else:
				if filtro == 1:

					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
										.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.is_eligible == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Disciplina, Arquivo.disciplina_id == Disciplina.id)\
								.filter(Disciplina.nome.like('%'+pesquisa+'%'))\
								.filter(Arquivo.is_eligible == True)\
								.paginate(page=page, per_page=12)
				
				if filtro == 2:
					
					existe_arquivo = db.session.query(Arquivo)\
										.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
										.filter(Professor.nome.like('%'+pesquisa+'%'))\
										.filter(Arquivo.is_eligible == True).first()
					arquivos = db.session.query(Arquivo)\
								.outerjoin(Professor, Arquivo.professor_id == Professor.id)\
								.filter(Professor.nome.like('%'+pesquisa+'%'))\
								.filter(Arquivo.is_eligible == True)\
								.paginate(page=page, per_page=12)

				if filtro is 3:
					existe_arquivo = Arquivo.query.filter_by(tipo_conteudo=tip_arquiv)\
									.filter_by(is_eligible=True).first()
					arquivos = Arquivo.query.filter_by(is_eligible=True)\
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

			return render_template('busca_assincrona_normal.html',tip_arquiv=tip_arquiv, arquivos=arquivos, 
				 	arquivos_rows=arquivos_rows, 
				existe_arquivo=existe_arquivo, navigation_data=navigation_data)
	
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

	print(arquivos_rows)

	return render_template('busca_assincrona_{}.html'.format(navigation_data[1]), tip_arquiv="all", arquivos=arquivos ,
			arquivos_rows=arquivos_rows, 
		existe_arquivo=existe_arquivo, navigation_data=navigation_data)