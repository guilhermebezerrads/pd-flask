from compleaks.disciplinas.models import Materia
from compleaks.questoes.models import Questao
import random

class Simulado(object):
	"""docstring for Simulado"""
	def __init__(self, n_quests, materias):
		self.n_quests = n_quests
		self.materias = materias
		self.atual = 0
		self.questoes = []
		self.resposta = []
	
	@staticmethod
	def quant_materia(mater):

		questoes = Questao.query.filter_by(ativado=True).filter_by(disciplina_id=mater.disciplina_id)\
								.filter_by(materia_id=mater.id)
		qtn_quest = 0

		for quest in questoes:
			qtn_quest = qtn_quest + 1

		return qtn_quest

	def acerto_por_materia(self, mate):
		acertos = 0
		contador = 0
		i = 0
		#mater = Materia.query.get_or_404(materia_id)

		for quest in self.questoes:
			if qust.materia_id = mate
				contador = contador + 1
				if quest.correta == self.resposta[i]:
					acertos = acertos + 1
				i = i + 1

		return acertos, contador, str(round((acertos/contador)*100))+"%"

	def gera_qustoes(self):

		questoes = []
		for mat in self.materias:
			qst = Questao.query.filter_by(ativado=True).filter_by(materia_id=int(mat))
			aux = []
			for qt in qst:
				aux.append(qt)
			questoes.append(aux)

		i = 0
		while i < self.n_quests:
			for lista in questoes:
				if lista:
					qust = random.randint(0, (len(lista)-1))
					self.questoes.append(lista[qust] )
					del lista[qust]
					i = i +1

	def gera_relatorio(self):
		i = 0
		corretas = 0
		for qust in self.questoes:
			if quest.correta == self.resposta[i]:
				corretas = corretas + 1
			i = i + 1
		
		relatorio.corretas = corretas

		relatorio.desmpenho = str(round((corretas/self.n_quests)*100))+"%"

		relacao = []
		for mate in self.materias:
			if int(mate) > 0
				nome = Materia.query.get_of_404(mate)
				relacao.append((nome, self.acerto_por_materia(mate)))

		relatorio.relacao = relacao

		return relatorio

	def next_quest(self):
		self.atual = self.atual + 1

	def quest(self):
		return self.questoes[self.atual]
		