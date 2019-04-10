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

	#print(request.referrer.split("/")[-1])
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
		print(simula.n_quests)
		simula.gera_qustoes()
		print(simula.materias)

		#session['simulado'] = simula
		session['quest_atual'] = 0

		return redirect(url_for('simulados.quest',
								 quest=0))

	return render_template('cria_simulado.html', form=form)


@simulados.route('/questao/<int:quest>', methods=['POST', 'GET'])
@login_required
def quest(quest):
	return "render_template('cria_simulado.html', form=form)"


@simulados.route('/finaliza-simulado')
@login_required
def finaliza():
	pass


@simulados.route('/numero-questao/<int:id>', methods=['POST', 'GET'])
@login_required
def numero_quest(id):
	
	disciplina = Disciplina.query.get_or_404(id)

	if not disciplina.ativado:
		abort(403)

	qtn_quest = quest_disciplina(disciplina.id)

	if qtn_quest < 3:
		abort(403)

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


	questoes = quest_disciplina(id)

	if questoes < 3:
		abort(403)

	materias = db.session.query(Materia)\
						.outerjoin(Questao, Materia.disciplina_id == Questao.disciplina_id )\
						.filter(Questao.disciplina_id == disciplina.id)

	qtn = 0

	for mat in materias:
		qtn = qtn + 1

	for mater in materias:
		mater.qtn = quant_materia(mater)

	materias_lista = [(str(materia.id), materia.nome, str(materia.qtn)) for materia in materias]

	questoes = Questao.query.filter_by(ativado=True).filter_by(materia_id=0)
	qtn_quest = 0

	for quest in questoes:
		qtn_quest = qtn_quest + 1
	

	if questoes > 15:
		questoes = 15

	return render_template('repositorio_materias_relacionadas.html', quantidade=questoes,
							 materias_lista=materias_lista, num_materias=qtn, sem_materia=qtn_quest)
