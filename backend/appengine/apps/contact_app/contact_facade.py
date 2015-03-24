# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from contact_app.contact_commands import ListContactCommand, SaveContactCommand, UpdateContactCommand, ContactForm,\
    GetContactCommand, DeleteContactCommand


def save_contact_cmd(**contact_properties):
    """
    Command to save Contact entity
    :param contact_properties: a dict of properties to save on model
    :return: a Command that save Contact, validating and localizing properties received as strings
    """
    return SaveContactCommand(**contact_properties)


def update_contact_cmd(contact_id, **contact_properties):
    """
    Command to update Contact entity with id equals 'contact_id'
    :param contact_properties: a dict of properties to update model
    :return: a Command that update Contact, validating and localizing properties received as strings
    """
    return UpdateContactCommand(contact_id, **contact_properties)


def list_contacts_cmd():
    """
    Command to list Contact entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListContactCommand()


def contact_form(**kwargs):
    """
    Function to get Contact's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return ContactForm(**kwargs)


def get_contact_cmd(contact_id):
    """
    Find contact by her id
    :param contact_id: the contact id
    :return: Command
    """
    return GetContactCommand(contact_id)



def delete_contact_cmd(contact_id):
    """
    Construct a command to delete a Contact
    :param contact_id: contact's id
    :return: Command
    """
    return DeleteContactCommand(contact_id)

