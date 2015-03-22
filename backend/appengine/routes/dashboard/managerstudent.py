from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router

__author__ = 'Samara Cardoso'


@login_not_required
@no_csrf
def index():
   return TemplateResponse(template_path='/contact/home.html')