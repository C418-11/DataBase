# -*- coding: utf-8 -*-

from .ABC import Event
from .ABC import RegEvent
from database.ABC import ABCServer


@RegEvent
class InitDataBase(Event):
    raw = "DATABASE.INIT"

    def __init__(self, database):
        self.database = database

    def func(self, server: ABCServer, **_kwargs):
        server.DBs.add(server.database(self.database, server.name))


INIT = InitDataBase

__all__ = ("INIT", )
