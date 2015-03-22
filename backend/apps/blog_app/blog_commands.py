# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from blog_app.blog_model import Blog



class BlogSaveForm(ModelForm):
    """
    Form used to save and update Blog
    """
    _model_class = Blog
    _include = [Blog.text, 
                Blog.title, 
                Blog.subject, 
                Blog.file, 
                Blog.author]


class BlogForm(ModelForm):
    """
    Form used to expose Blog's properties for list or json
    """
    _model_class = Blog


class GetBlogCommand(NodeSearch):
    _model_class = Blog


class DeleteBlogCommand(DeleteNode):
    _model_class = Blog


class SaveBlogCommand(SaveCommand):
    _model_form_class = BlogSaveForm


class UpdateBlogCommand(UpdateNode):
    _model_form_class = BlogSaveForm


class ListBlogCommand(ModelSearchCommand):
    def __init__(self):
        super(ListBlogCommand, self).__init__(Blog.query_by_creation())

