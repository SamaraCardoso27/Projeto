# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from gallery_app.gallery_commands import ListGalleryCommand, SaveGalleryCommand, UpdateGalleryCommand, GalleryForm,\
    GetGalleryCommand, DeleteGalleryCommand


def save_gallery_cmd(**gallery_properties):
    """
    Command to save Gallery entity
    :param gallery_properties: a dict of properties to save on model
    :return: a Command that save Gallery, validating and localizing properties received as strings
    """
    return SaveGalleryCommand(**gallery_properties)


def update_gallery_cmd(gallery_id, **gallery_properties):
    """
    Command to update Gallery entity with id equals 'gallery_id'
    :param gallery_properties: a dict of properties to update model
    :return: a Command that update Gallery, validating and localizing properties received as strings
    """
    return UpdateGalleryCommand(gallery_id, **gallery_properties)


def list_gallerys_cmd():
    """
    Command to list Gallery entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListGalleryCommand()


def gallery_form(**kwargs):
    """
    Function to get Gallery's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return GalleryForm(**kwargs)


def get_gallery_cmd(gallery_id):
    """
    Find gallery by her id
    :param gallery_id: the gallery id
    :return: Command
    """
    return GetGalleryCommand(gallery_id)



def delete_gallery_cmd(gallery_id):
    """
    Construct a command to delete a Gallery
    :param gallery_id: gallery's id
    :return: Command
    """
    return DeleteGalleryCommand(gallery_id)

