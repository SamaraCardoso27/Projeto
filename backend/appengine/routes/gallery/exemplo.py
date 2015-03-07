from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router

__author__ = 'Samara Cardoso'


@login_not_required
@no_csrf
def index(_handler):
    path = router.to_path(funcao)
    _handler.redirect(path)


@login_not_required
@no_csrf
def funcao(_resp, nome,sobrenome='Hans'):
    _resp.write('%s %s ' %(nome,sobrenome))