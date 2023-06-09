# -*- coding: utf-8 -*-

from .ABC import Event
from .ABC import RegEvent
from database.ABC import ABCServer


@RegEvent
class InitDataBase(Event):
    raw = "DATABASE.INIT"

    def __init__(self, database, name):
        self.database = database
        self.name = name

    def func(self, server: ABCServer, **_kwargs):
        server.DBs.add(server.databases[self.database](self.name, server.name))


INIT = InitDataBase

__all__ = ("INIT", )
