from flask import (render_template, Blueprint, url_for, redirect,
 					flash, current_app, request, abort)
from compleaks import db
from flask_login import current_user, login_required
from compleaks.disciplinas.models import Disciplina
from compleaks.questoes.models import  Questao, Alternativa
from compleaks.questoes.forms import AdicionarQuestaoForm

questoes = Blueprint('questoes', __name__,template_folder='templates/questoes')

@questoes.route('/adicionar', methods=['POST', 'GET'])
@login_required
def adicionar():
	form = AdicionarQuestaoForm()

	form.disciplina.choices = [(str(disciplina.id), disciplina.nome)
									 for disciplina in Disciplina.query.order_by('nome')
									 if disciplina.ativado]

	if form.validate_on_submit():

		#dados gerais
		disciplina = int(form.disciplina.data)
		enunciado = form.enunciado.data
		correta = int(form.correta.data)

		new_quest = Questao(enunciado=enunciado, disciplina_id=disciplina,
		 					usuario_id=current_user.id, correta=correta)

		db.session.add(new_quest)
		db.session.commit()

		quest = Questao.query.order_by(Questao.data_criacao.desc()).first()

		#alternativa a)
		conteudo = form.opcao_a.data
		alter_a = Alternativa(conteudo=conteudo, questao_id=quest.id, opcao=1)

		#alternativa b)
		conteudo = form.opcao_b.data
		alter_b = Alternativa(conteudo=conteudo, questao_id=quest.id, opcao=2)

		#alternativa c)
		conteudo = form.opcao_c.data
		alter_c = Alternativa(conteudo=conteudo, questao_id=quest.id, opcao=3)

		#alternativa d)
		conteudo = form.opcao_d.data
		alter_d = Alternativa(conteudo=conteudo, questao_id=quest.id, opcao=4)

		db.session.add_all([alter_d, alter_c, alter_b, alter_a])
		db.session.commit()

	flash("Questao cadastrada com sucesso", "success")

	return render_template('adicionar_questao.html', form=form)

@questoes.route('/buscar', methods=['POST', 'GET'])
@login_required
def buscar():

	return render_template('buscar_questao.html')

@questoes.route('/editar/<id>', methods=['POST', 'GET'])
@login_required
def editar(id):

	return render_template('editar_questao.html')

@questoes.route('/excluir/<id>', methods=['POST', 'GET'])
@login_required
def excluir(id):

	pass

@questoes.route('/restaurar/<id>', methods=['POST', 'GET'])
@login_required
def restaurar(id):

	pass