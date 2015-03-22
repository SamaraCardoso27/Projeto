# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from contact_app.contact_model import Contact



class ContactSaveForm(ModelForm):
    """
    Form used to save and update Contact
    """
    _model_class = Contact
    _include = [Contact.message, 
                Contact.email, 
                Contact.name]


class ContactForm(ModelForm):
    """
    Form used to expose Contact's properties for list or json
    """
    _model_class = Contact


class GetContactCommand(NodeSearch):
    _model_class = Contact


class DeleteContactCommand(DeleteNode):
    _model_class = Contact


class SaveContactCommand(SaveCommand):
    _model_form_class = ContactSaveForm


class UpdateContactCommand(UpdateNode):
    _model_form_class = ContactSaveForm


class ListContactCommand(ModelSearchCommand):
    def __init__(self):
        super(ListContactCommand, self).__init__(Contact.query_by_creation())

