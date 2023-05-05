# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1"

import json
from typing import Union

from database.ABC import ABCServer
from database.ABC import Event
from database.ABC import MKEvent
from database.ABC import NameList
from database.ABC import RunSuccess
from database.logging import INFO


def WriteJson(server: ABCServer, arg: dict, file_name: str):
    data = json.dumps(arg, indent=4)
    with open(server.path + file_name, encoding='utf-8', mode='w', newline='\n') as file:
        file.write(data)


def GetUsers(server: ABCServer) -> Union[dict, str]:
    """
    :param server: 数据库服务器
    :return: 用户注册表对象
    """

    try:
        users = json.load(open(server.path + server.USERDATA_FILE, encoding='utf-8', mode='r'))  # 加载用户名单
        return users
    except FileNotFoundError:
        WriteJson(server=server, arg={"default": {"password": "default"}}, file_name=server.USERDATA_FILE)

        users = json.load(open(server.path + server.USERDATA_FILE, encoding='utf-8', mode='r'))  # 加载用户名单
        return users


class AckUserAndPassword(Event):
    raw = "ACK_USER_AND_PASSWORD"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def func(self, server: ABCServer, **_kwargs):
        """
        :return: USER_NOT_FIND | WRONG_PASSWORD | LOGIN_SUCCESS
        """

        server.log(msg=f"{self.username} Try Login username={self.username} password={self.password}", level=INFO)

        users = GetUsers(server=server)

        if self.username not in users.keys():  # 判断是否有此账户
            return USER_NOT_FIND

        user_info = users[self.username]
        user_info: dict

        if self.password != user_info["password"]:  # 判断密码是否正确
            return WRONG_PASSWORD

        server.log(msg=f"{self.username} Success Login username={self.username} info={user_info}", level=INFO)
        return LOGIN_SUCCESS


class LoginSuccess(RunSuccess):
    raw = "LOGIN_SUCCESS"


LOGIN_SUCCESS = LoginSuccess()

USER_NOT_FIND = MKEvent("USER_NOT_FIND")
WRONG_PASSWORD = MKEvent("WRONG_PASSWORD")

USER_ALREADY_EXISTS = MKEvent("USER_ALREADY_EXISTS")


class RegUser(Event):
    raw = "REG_USER"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def func(self, server: ABCServer, **_kwargs):
        users = GetUsers(server=server)
        try:
            users[self.username]
        except KeyError:
            pass
        else:
            return USER_ALREADY_EXISTS

        users[self.username] = {"password": self.password}

        WriteJson(server=server, arg=users, file_name=server.USERDATA_FILE)


class ReSetPassword(Event):
    raw = "RESET_PASSWORD"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def func(self, server: ABCServer, **_kwargs):
        users = GetUsers(server=server)

        if self.username not in users.keys():
            return USER_NOT_FIND
        users[self.username]["password"] = self.password

        WriteJson(server=server, arg=users, file_name=server.USERDATA_FILE)


class DelUser(Event):
    raw = "DEL_USER"

    def __init__(self, username: str):
        self.username = username

    def func(self, server: ABCServer, **_kwargs):
        users = GetUsers(server=server)
        if self.username not in users.keys():
            return USER_NOT_FIND

        del users[self.username]

        WriteJson(server=server, arg=users, file_name=server.USERDATA_FILE)


class InitDataBase(Event):
    raw = "INIT_DATABASE"

    def __init__(self, database):
        self.database = database

    def func(self, server: ABCServer, **_kwargs):
        server.DBs.add(server.DataBase(self.database, server.name))


class CreateDataBase(Event):
    raw = "CREATE_DATABASE"

    def __init__(self, database, store):
        self.database = database
        self.store = store

    def func(self, server: ABCServer, **_kwargs):
        db_obj = server[self.database]
        db_obj.create(self.store)


class SetDataBaseFormat(Event):
    raw = "SET_DATABASE_FORMAT"

    def __init__(self, database, store, format_: NameList):
        self.database = database
        self.store = store
        self.format_ = format_

    def func(self, server: ABCServer, **_kwargs):
        db_obj = server[self.database]
        db_obj[self.store].set_format(self.format_)


class DebugEvent(Event):
    raw = "DEBUG"

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def func(self, server: ABCServer, **_kwargs):
        print("DEBUG_EVENT(server={}, event={}, kwargs={})".format(server, self, _kwargs))


__all__ = (
    "AckUserAndPassword",
    "LOGIN_SUCCESS",
    "USER_NOT_FIND",
    "WRONG_PASSWORD",
    "USER_ALREADY_EXISTS",
    "RegUser",
    "ReSetPassword",
    "DelUser",
    "InitDataBase",
    "CreateDataBase",
    "SetDataBaseFormat",
    "DebugEvent"
)
