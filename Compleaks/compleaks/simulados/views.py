from flask import (render_template, Blueprint, url_for,
					redirect, flash, abort, request, session)
from flask_login import current_user, login_required
from compleaks import db
from compleaks.questoes.forms import (ComentarioQuestaoForm, ExcluirComentarioQuestaoForm,
									 EditarComentarioQuestaoForm, ResponderComentarioQuestaoForm)
from compleaks.simulados.forms import (CriarSimuladoForm)
from compleaks.simulados.models import Simulado
from compleaks.usuarios.models import Usuario
from compleaks.disciplinas.models import Disciplina, Materia
from compleaks.questoes.models import Questao

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

		if  quantidade < 3 or quantidade > 15:
			abort(403)

		if not materias:
			abort(403)

		for mat in materias:
			if mat > 0:
				mater = Materia.query.get_or_404(mat)
				disc = Disciplina.query.get_or_404(mater.disciplina_id)
			
				if not disc.ativado:
					abort(403)

		simula = Simulado(n_quests=quantidade, materias=materias)
		simula.gera_qustoes()

		current_user.simulado = simula
		current_user.quest_atual = 0

		return redirect(url_for('simulados.quest'))

	return render_template('cria_simulado.html', form=form)


@simulados.route('/questao', methods=['POST', 'GET'])
@login_required
def quest():

	try:
		if not current_user.simulado:
			abort(403)

	except:
		abort(403)

	try:
		if (current_user.simulado.atual == 0) and (str(request.referrer.split("/")[-1]) != "novo"):
			abort(403)
		elif str(request.referrer.split("/")[-2]) != "questao":
			abort(403)

	except:
		abort(403)

	if str(request.referrer.split("/")[-2]) == "questao":
		current_user.simulado.next_quest()

	if current_user.simulado.atual  >= current_user.simulado.n_quests:
		relatorio = current_user.simulado.gera_relatorio()
		return render_template('resultado_simulado.html', relatorio=relatorio)


	return render_template('faz_questao.html', quest=current_user.simulado.quest() )


@simulados.route('/finaliza-simulado')
@login_required
def finaliza():
	pass


@simulados.route('/numero-questao/<int:id>/<int:n1>/<int:n2>/<int:n3>', methods=['POST', 'GET'])
@simulados.route('/numero-questao/<int:id>', defaults={"n1":-1, "n2":0,"n3":0}, methods=['POST', 'GET'])
@login_required
def numero_quest(id, n1, n2, n3):
	
	disciplina = Disciplina.query.get_or_404(id)
	if not disciplina.ativado:
			abort(403)
	
	qtn_quest = 0
	print(n1)
	
	if n1 < 0:
		qtn_quest = quest_disciplina(disciplina.id)

	else:
		mate =[n1, n2, n3]
		maters = set(mate)

		materias = []

		for mat in maters:
			materias.append(Materia.query.get_or_404(mat))

		for mater in materias:
			qtn_quest = qtn_quest + quant_materia(mater)

	if qtn_quest > 15:
		qtn_quest = 15

	return render_template('repositorio_qtn_quest.html', quantidade=qtn_quest)


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
		print(mat.nome)
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

