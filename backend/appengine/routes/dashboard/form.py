from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router

__author__ = 'Samara Cardoso'


@login_not_required
@no_csrf
def index():
    contexto = {'save_path': router.to_path(salvar)}
    return TemplateResponse(contexto)


@login_not_required
def salvar(_resp, nome):
    _resp.write(nome)

