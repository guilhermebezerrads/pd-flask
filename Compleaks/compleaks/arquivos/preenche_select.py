from compleaks.disciplinas.models import Disciplina
from compleaks.professores.models import Professor
from compleaks.arquivos.models import Arquivo
from compleaks.usuarios.models import Usuario


class Preenche():

    def listaDiciplinas(self):
        todas_disc = Disciplina.query.all()
        lista_form = []
        for diciplin in todas_disc:
            lista_form.append((str(diciplin.id), diciplin.nome))
        return lista_form

    def listaProfessores(self):
        todos_profs = Professor.query.all()
        lista_form = []
        for prof in todos_profs:
            lista_form.append((str(prof.id), prof.nome))
        return lista_form