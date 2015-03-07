from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required

__author__ = 'Samara Cardoso'

@login_not_required
@no_csrf
def index(nome='Samara', sobrenome='Cardoso'):
    class Pessoa(object):
        def __init__(self,nome,sobrenome):
            self.nome = nome
            self.sobrenome = sobrenome
    pessoas = [Pessoa('Samara','Cardoso'),Pessoa('Daiana','Cardoso')]

    contexto ={'name':nome, 'pessoas':pessoas}
    return TemplateResponse(contexto)