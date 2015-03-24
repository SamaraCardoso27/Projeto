# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class Stundet(Node):
    name = ndb.StringProperty(required=True)
    birthday = ndb.DateProperty(required=True)
    phone_number = ndb.StringProperty(required=True)
    course = ndb.StringProperty(required=True)

