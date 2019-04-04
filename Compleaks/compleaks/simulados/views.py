from flask import render_template, Blueprint, url_for, redirect, flash, abort, request
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

	form = CriarSimuladoForm()

	form.disciplina.choices = [(str(disciplina.id), disciplina.nome)
								for disciplina in Disciplina.query.order_by('nome')
								if disciplina.ativado and quest_disciplina(disciplina.id) >= 3]

	'''
	for disciplina in form.disciplina.choices
		questoes = len(Questao.query.filter_by(ativado=True).filter_by(disciplina_id=id))

		if questoes < 3:
			form.disciplina.choices.remove((str(disciplina.id), disciplina.nome))
	'''

	if form.validate_on_submit():
		pass

	return render_template('cria_simulado.html', form=form)

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

	print(questoes)

	return render_template('repositorio_qtn_quest.html', quantidade=qtn_quest)

@simulados.route('/materias-possiveis/<int:id>', methods=['POST', 'GET'])
@login_required
def materias(id):
	
	disciplina = Disciplina.query.get_or_404(id)

	if not disciplina.ativado:
		abort(403)


	questoes = len(Questao.query.filter_by(ativado=True).filter_by(disciplina_id=id))

	if questoes < 3:
		abort(403)

	materias = db.session.query(Materia)\
						.outerjoin(Questao, Materia.disciplina_id == Questao.disciplina_id )\
						.filter(Questao.disciplina_id == disciplina.id)

	materias_lista = [(str(materia.id), materia.nome) for materia in materias]
	print(materias)

	if questoes > 15:
		questoes = 15

	return render_template('repositorio_materias_relacionadas.html', quantidade=questoes,
							 materias_lista=materias_lista, numero_materias=len(materias))
