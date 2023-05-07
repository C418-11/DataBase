# -*- coding: utf-8 -*-

from .ABC import Event
from .ABC import RegEvent
from database.ABC import ABCServer
from database.ABC import NameList


@RegEvent
class CreateStore(Event):
    raw = "STORE.CREATE_STORE"

    def __init__(self, database, store):
        self.database = database
        self.store = store

    def func(self, server: ABCServer, **_kwargs):
        db_obj = server[self.database]
        db_obj.create(self.store)


CREATE = CreateStore


@RegEvent
class SetStoreFormat(Event):
    raw = "STORE.SET_STORE_FORMAT"

    def __init__(self, database, store, format_: NameList):
        self.database = database
        self.store = store
        self.format_ = format_

    def func(self, server: ABCServer, **_kwargs):
        db_obj = server[self.database]
        db_obj[self.store].set_format(self.format_)


SET_FORMAT = SetStoreFormat


@RegEvent
class SetHistoryFormat(Event):
    raw = "STORE.SET_HISTORY_FORMAT"

    def __init__(self, database, store, format_: str):
        self.database = database
        self.store = store
        self.format_ = format_

    def func(self, server: ABCServer, **_kwargs):
        db_obj = server[self.database]
        db_obj[self.store].set_history_format(self.format_)


SET_HISTORY_FORMANT = SetHistoryFormat


@RegEvent
class Append(Event):
    raw = "STORE.APPEND"

    def __init__(self, database, store, line: NameList):
        self.database = database
        self.store = store
        self.line = line

    def func(self, server: ABCServer, **_kwargs):
        db_obj = server[self.database]
        store_obj = db_obj[self.store]
        store_obj.append(self.line)


APPEND = Append


@RegEvent
class GetLine(Event):
    raw = "STORE.GET_LINE"

    def __init__(self, database, store, index):
        self.database = database
        self.store = store
        self.index = index

    def func(self, server: ABCServer, **_kwargs):
        db_obj = server[self.database]
        store_obj = db_obj[self.store]
        return store_obj[self.index]


GET_LINE = GetLine


@RegEvent
class SetLine(Event):
    raw = "STORE.SET_LINE"

    def __init__(self, database, store, index: int, line: NameList):
        self.database = database
        self.store = store
        self.index = index
        self.line = line

    def func(self, server: ABCServer, **_kwargs):
        db_obj = server[self.database]
        store_obj = db_obj[self.store]
        store_obj[self.index] = self.line.ToDict()


SET_LINE = SetLine


@RegEvent
class DelLine(Event):
    raw = "STORE.DEL_LINE"

    def __init__(self, database, store, index: int):
        self.database = database
        self.store = store
        self.index = index

    def func(self, server: ABCServer, **_kwargs):
        db_obj = server[self.database]
        store_obj = db_obj[self.store]
        del store_obj[self.index]


DEL_LINE = DelLine

__all__ = ("CREATE", "SET_FORMAT", "SET_HISTORY_FORMANT", "APPEND", "GET_LINE", "SET_LINE", "DEL_LINE")
