from flask import (render_template, Blueprint, url_for,
					redirect, flash, abort, request, session)
from flask_login import current_user, login_required
from compleaks import db
from compleaks.questoes.forms import (ComentarioQuestaoForm, ExcluirComentarioQuestaoForm,
									 EditarComentarioQuestaoForm, ResponderComentarioQuestaoForm)
from compleaks.simulados.forms import (CriarSimuladoForm)
#from compleaks.simulados.models import Simulado
from compleaks.usuarios.models import Usuario
from compleaks.disciplinas.models import Disciplina, Materia
from compleaks.questoes.models import Questao, Alternativa
from compleaks.questoes.forms import  FazerQuestaoForm
import random

simulados = Blueprint('simulados', __name__,template_folder='templates/simulados')

def quest_disciplina(id):

	questoes = Questao.query.filter_by(ativado=True).filter_by(disciplina_id=id)
	qtn_quest = 0

	for quest in questoes:
		qtn_quest = qtn_quest + 1

	return qtn_quest

@simulados.route('/novo', methods=['POST', 'GET'])
@login_required
def criar():

	#print(request.referrer.split("/")[0])
	#print(request.form.get("m1"))

	form = CriarSimuladoForm()

	form.disciplina.choices = [(str(disciplina.id), disciplina.nome)
								for disciplina in Disciplina.query.order_by('nome')
								if disciplina.ativado and quest_disciplina(disciplina.id) >= 3]

	materias = []
	if form.validate_on_submit():

		for i in range(3):
			if request.form.get("m"+str(i+1)):

				try:
					#print("m"+str(i+1))
					#print(int(request.form.get("m"+str(i+1))))
					materias.append(int(request.form.get("m"+str(i+1))))
				except:
					abort(403)

		quantidade = 0
		if request.form.get("Quantidad"):
			qtn = request.form.get("Quantidad")
			try:
				quantidade = int(qtn)
			except:
				abort(403)

		if  quantidade < 0 or quantidade > 15:
			abort(403)

		if not materias:
			abort(403)

		for mat in materias:
			if mat > 0:
				mater = Materia.query.get_or_404(mat)
				disc = Disciplina.query.get_or_404(mater.disciplina_id)
			
				if not disc.ativado:
					abort(403)

		aux = set(materias.copy())
		materias.clear()
		for mat in aux:
			if mat > 0:
				materias.append(mat)

		session['n_quests'] = quantidade
		session['materias'] = materias
		session['disc'] = disc.id
		session['atual'] = 0
		session['questoes'] = []
		session['resposta'] = {}
		gera_qustoes()
		'''
		print(session['materias'])
		print(session['disc'])
		print(session['resposta'])
		print(session['questoes'])
		'''
		return redirect(url_for('simulados.quest'))

	return render_template('cria_simulado.html', form=form)


@simulados.route('/questao', methods=['POST', 'GET'])
@login_required
def quest():

	next_quest()
	form_questao = FazerQuestaoForm()

	if session['atual']  <= session['n_quests']:
		alternativas = Alternativa.query.filter(Alternativa.questao_id.contains(session['questoes'][session['atual']-1]))
	
	else:
		alternativas = Alternativa.query.filter(Alternativa.questao_id.contains(session['questoes'][session['atual']-2]))

	obj_alter = []

	for altern in alternativas:
		obj_alter.append(altern)

	form_questao.radio_alternativas.choices = [(str(alternativa.opcao), alternativa.conteudo)
									 for alternativa in obj_alter]

	form_questao.radio_alternativas.choices = [(str(alternativa.opcao), alternativa.conteudo)
									 for alternativa in obj_alter]					 

	try:
		if not session['disc'] or not session['materias'] or not session['questoes']:
			print("1")
			abort(403)

	except:
		abort(403)

	try:
		if (session['atual'] == 1) and (str(request.referrer.split("/")[-1]) != "novo"):
			print(request.referrer.split("/")[-1])
			print("2")
			abort(403)
		elif (session['atual'] > 1) and (str(request.referrer.split("/")[-1]) != "questao"):
			print("3")
			abort(403)

	except:
		print("4")
		abort(403)

	if form_questao.validate_on_submit():
		quest = Questao.query.get(session['questoes'][session['atual']-2])
		session['resposta'].update({str(quest.id): int(form_questao.radio_alternativas.data)})

	if session['atual']  > session['n_quests']:
		return redirect(url_for('simulados.finaliza'))

	quest = Questao.query.get(session['questoes'][session['atual']-1])

	#print(session['resposta'])

	return render_template('faz_questao.html', quest=quest,
							 form_questao=form_questao, number_quest=session['atual'])


@simulados.route('/finaliza-simulado')
@login_required
def finaliza():
	relatorio = gera_relatorio()
	return render_template('resultado_simulado.html', relatorio=relatorio)


@simulados.route('/numero-questao/<int:id>/<string:N>', methods=['POST', 'GET'])
@login_required
def numero_quest(id, N):
	try:
		n1 = int(N.split("%")[0])
		n2 = int(N.split("%")[1])
		n3 = int(N.split("%")[2])
	except:
		abort(403)
	disciplina = Disciplina.query.get_or_404(id)
	if not disciplina.ativado:
			abort(403)
	
	qtn_quest = 0
	
	if n1 < 0:
		qtn_quest = quest_disciplina(disciplina.id)

	else:
		mate = [n1, n2, n3]
		maters = set(mate)

		materias = []

		for mat in maters:
			if mat > 0:
				materias.append(Materia.query.get_or_404(mat))

		for mater in materias:
			qtn_quest = qtn_quest + quant_materia(mater)

	if qtn_quest > 15:
		qtn_quest = 15

	return render_template('repositorio_qtn_quest.html', quantidade=qtn_quest)

#################################################
########### SIMULADOS ###########################
#################################################

def acerto_por_materia(materia_id):
	acertos = 0
	contador = 0
	questoes = []

	for ids in session['questoes']:
		quest = Questao.query.get(ids)
		questoes.append(quest)

	for quest in questoes:
		if quest.materia_id == materia_id:
			contador = contador + 1
			if quest.correta == session['resposta'][str(quest.id)]:
				acertos = acertos + 1

	return acertos, contador, int(round(float(acertos/contador)*100)) 

def gera_qustoes():

	quests = []
	for mat in session['materias']:
		qst = Questao.query.filter_by(ativado=True).filter_by(materia_id=int(mat))
		aux = []
		for qt in qst:
			aux.append(qt)
		quests.append(aux)

	if session['materias'] is not None:

		i = 0
		while i < session['n_quests']:
			for lista in quests:
				if lista:
					qust = random.randint(0, (len(lista)-1))
					session['questoes'].append(lista[qust].id)
					del lista[qust]
					i = i + 1

	else:

		all_qust = todas_possiveis() 
		i = 0
		while i < session['n_quests']:
			qust = random.randint(0, (len(all_qust)-1))
			session['questoes'].append(lista[qust].id)

class Relatorio(object):
	pass	

def gera_relatorio():

	relatorio = Relatorio()

	questoes = []
	for ids in session['questoes']:
		quest = Questao.query.get(ids)
		questoes.append(quest)

	#print(session['resposta'])

	relacao = []
	for mate in session['materias']:
		if int(mate) > 0:
			nome = Materia.query.get_or_404(mate)
			relacao.append((nome, acerto_por_materia(mate)))

	relatorio.relacao = relacao

	corretas = 0
	for reltion in relacao:
		corretas = corretas + reltion[1][0]
	
	#print(corretas)
	relatorio.corretas = corretas


	#O Doughbut infelizmente é material PRO
	relatorio.desmpenho = int(round((corretas/session['n_quests'])*100))	
	relatorio.finalLabel = relatorio.relacao[2][0]
	relatorio.finalData = relatorio.relacao[2][1]
	relatorio.doughnut = [[],[],[],[]]
	relatorio.doughnut[0] = ["#F7464A", "#46BFBD", "#FDB45C"]
	relatorio.doughnut[1] = "#FDB45C"
	relatorio.doughnut[2] = ["#FF5A5E", "#5AD3D1", "#FFC870"]
	relatorio.doughnut[3] = "#FFC870"


	#Gera os dados para o gráfico de acertos por matéria
	relatorio.label_final = relatorio.relacao[2][0].nome
	relatorio.data_final = relatorio.relacao[2][1][2]
	relatorio.sidebarData = [relac[1][2] for relac in relatorio.relacao]
	relatorio.sidebarLabel = [(relac[0].nome[:9] + '..') if len(relac[0].nome) > 11 else relac[0].nome for relac in relatorio.relacao ]
	colors = []

	for relac in relatorio.relacao:
		if relac[1][2] >= 60:
			colors.append("rgba(54, 162, 235, 0.2)")
		else:
			colors.append("rgba(255, 99, 132, 0.2)")

	relatorio.sidebarColors = colors
	#relatorio.sidebar[3] = "#FFC870"

	return relatorio

def next_quest():
	session['atual'] = session['atual'] + 1

def todas_possiveis():
	questoes = Questao.query.filter_by(ativado=True).filter_by(disciplina_id=self.disc)

	aux = []
	for quest in questoes:
		aux.append(quest)

	return aux

#################################################
########### SIMULADOS ###########################
#################################################


def quant_materia(mater):

	questoes = Questao.query.filter_by(ativado=True).filter_by(disciplina_id=mater.disciplina_id)\
							.filter_by(materia_id=mater.id)
	qtn_quest = 0

	for quest in questoes:
		qtn_quest = qtn_quest + 1

	return qtn_quest


@simulados.route('/materias-possiveis/<int:id>', methods=['POST', 'GET'])
@login_required
def materias(id):

	disciplina = Disciplina.query.get_or_404(id)

	if not disciplina.ativado:
		abort(403)

	mats = db.session.query(Materia)\
						.outerjoin(Questao, Materia.disciplina_id == Questao.disciplina_id )\
						.filter(Questao.disciplina_id == disciplina.id)

	materias = []

	for mat in mats:
		materias.append(mat)

	for mat in materias:
		if quant_materia(mat) == 0:
			materias.remove(mat)

	qtn = 0

	for mat in materias:
		qtn = qtn + 1

	quant = []

	for mater in materias:
		quant.append(quant_materia(mater))

	materias_lista = [[str(materia.id), materia.nome] for materia in materias]

	i = 0

	for lista in materias_lista:

		lista.append(str(quant[i]))
		i = i+1

	questoes = Questao.query.filter_by(ativado=True).filter_by(materia_id=0)
	qtn_quest = 0

	for quest in questoes:
		qtn_quest = qtn_quest + 1
	

	if qtn_quest > 15:
		qtn_quest = 15

	return render_template('repositorio_materias_relacionadas.html', quantidade=questoes,
							 materias_lista=materias_lista, num_materias=qtn, sem_materia=qtn_quest)

