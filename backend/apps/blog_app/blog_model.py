# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class Blog(Node):
    author = ndb.StringProperty(required=True)
    subject = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    text = ndb.StringProperty(required=True)
    file = ndb.StringProperty(required=True)

