# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class Gallery(ndb.Model):
    name_author = ndb.StringProperty(required=True)
    file = ndb.StringProperty(required=True)

