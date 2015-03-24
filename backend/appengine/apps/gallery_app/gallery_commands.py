# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from gallery_app.gallery_model import Gallery



class GallerySaveForm(ModelForm):
    """
    Form used to save and update Gallery
    """
    _model_class = Gallery
    _include = [Gallery.name_author, 
                Gallery.file]


class GalleryForm(ModelForm):
    """
    Form used to expose Gallery's properties for list or json
    """
    _model_class = Gallery


class GetGalleryCommand(NodeSearch):
    _model_class = Gallery


class DeleteGalleryCommand(DeleteNode):
    _model_class = Gallery


class SaveGalleryCommand(SaveCommand):
    _model_form_class = GallerySaveForm


class UpdateGalleryCommand(UpdateNode):
    _model_form_class = GallerySaveForm


class ListGalleryCommand(ModelSearchCommand):
    def __init__(self):
        super(ListGalleryCommand, self).__init__(Gallery.query_by_creation())

