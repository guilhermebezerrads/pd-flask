from flask import (render_template, Blueprint)

questoes = Blueprint('questoes', __name__,template_folder='templates/questoes')


@questoes.route('/adicionar', methods=['POST', 'GET'])
@login_required
def adicionar():

	return render_template('adicionar_questao.html')

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