# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from student_app.student_model import Stundet



class StundetSaveForm(ModelForm):
    """
    Form used to save and update Stundet
    """
    _model_class = Stundet
    _include = [Stundet.phone_number, 
                Stundet.course, 
                Stundet.birthday, 
                Stundet.name]


class StundetForm(ModelForm):
    """
    Form used to expose Stundet's properties for list or json
    """
    _model_class = Stundet


class GetStundetCommand(NodeSearch):
    _model_class = Stundet


class DeleteStundetCommand(DeleteNode):
    _model_class = Stundet


class SaveStundetCommand(SaveCommand):
    _model_form_class = StundetSaveForm


class UpdateStundetCommand(UpdateNode):
    _model_form_class = StundetSaveForm


class ListStundetCommand(ModelSearchCommand):
    def __init__(self):
        super(ListStundetCommand, self).__init__(Stundet.query_by_creation())

