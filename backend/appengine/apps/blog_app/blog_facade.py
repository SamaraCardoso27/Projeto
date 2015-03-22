# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from blog_app.blog_commands import ListBlogCommand, SaveBlogCommand, UpdateBlogCommand, BlogForm,\
    GetBlogCommand, DeleteBlogCommand


def save_blog_cmd(**blog_properties):
    """
    Command to save Blog entity
    :param blog_properties: a dict of properties to save on model
    :return: a Command that save Blog, validating and localizing properties received as strings
    """
    return SaveBlogCommand(**blog_properties)


def update_blog_cmd(blog_id, **blog_properties):
    """
    Command to update Blog entity with id equals 'blog_id'
    :param blog_properties: a dict of properties to update model
    :return: a Command that update Blog, validating and localizing properties received as strings
    """
    return UpdateBlogCommand(blog_id, **blog_properties)


def list_blogs_cmd():
    """
    Command to list Blog entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListBlogCommand()


def blog_form(**kwargs):
    """
    Function to get Blog's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return BlogForm(**kwargs)


def get_blog_cmd(blog_id):
    """
    Find blog by her id
    :param blog_id: the blog id
    :return: Command
    """
    return GetBlogCommand(blog_id)



def delete_blog_cmd(blog_id):
    """
    Construct a command to delete a Blog
    :param blog_id: blog's id
    :return: Command
    """
    return DeleteBlogCommand(blog_id)

