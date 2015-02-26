# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from book_app.book_model import Book



class BookSaveForm(ModelForm):
    """
    Form used to save and update Book
    """
    _model_class = Book
    _include = [Book.edition, 
                Book.price, 
                Book.title]


class BookForm(ModelForm):
    """
    Form used to expose Book's properties for list or json
    """
    _model_class = Book


class GetBookCommand(NodeSearch):
    _model_class = Book


class DeleteBookCommand(DeleteNode):
    _model_class = Book


class SaveBookCommand(SaveCommand):
    _model_form_class = BookSaveForm


class UpdateBookCommand(UpdateNode):
    _model_form_class = BookSaveForm


class ListBookCommand(ModelSearchCommand):
    def __init__(self):
        super(ListBookCommand, self).__init__(Book.query_by_creation())

