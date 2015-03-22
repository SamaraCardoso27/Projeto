# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from student_app.student_commands import ListStundetCommand, SaveStundetCommand, UpdateStundetCommand, StundetForm,\
    GetStundetCommand, DeleteStundetCommand


def save_stundet_cmd(**stundet_properties):
    """
    Command to save Stundet entity
    :param stundet_properties: a dict of properties to save on model
    :return: a Command that save Stundet, validating and localizing properties received as strings
    """
    return SaveStundetCommand(**stundet_properties)


def update_stundet_cmd(stundet_id, **stundet_properties):
    """
    Command to update Stundet entity with id equals 'stundet_id'
    :param stundet_properties: a dict of properties to update model
    :return: a Command that update Stundet, validating and localizing properties received as strings
    """
    return UpdateStundetCommand(stundet_id, **stundet_properties)


def list_stundets_cmd():
    """
    Command to list Stundet entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListStundetCommand()


def stundet_form(**kwargs):
    """
    Function to get Stundet's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return StundetForm(**kwargs)


def get_stundet_cmd(stundet_id):
    """
    Find stundet by her id
    :param stundet_id: the stundet id
    :return: Command
    """
    return GetStundetCommand(stundet_id)



def delete_stundet_cmd(stundet_id):
    """
    Construct a command to delete a Stundet
    :param stundet_id: stundet's id
    :return: Command
    """
    return DeleteStundetCommand(stundet_id)

