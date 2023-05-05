# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"

import json
import os
import pickle
from abc import ABC
from typing import BinaryIO
from typing import TextIO
from typing import Type
from typing import Union

from database.SocketIO import SocketIo


class NameList:
    def __init__(self, *args, **kwargs):
        self._attributes = dict()
        for name in args:
            self.__setattr__(name, None)
        for name, value in kwargs.items():
            self.__setattr__(name, value)

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        self._attributes[key] = value

    def __delattr__(self, item):
        del self._attributes[item]
        object.__delattr__(self, item)

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)


class ABCStore(ABC):
    path: str
    name: str
    _id: str
    format: Union[NameList, None]

    def __init__(self, __store_path: str, database):
        self.path = __store_path
        self.database = database

        BuildPath(path=self.path)

        self.info = database.BinJsonReader(self.path + self.database.INFO_FILE)

        self._id = self.info["id"]
        self.name = self.info["name"]
        format_ = self.info["format"]
        self.format = None
        if format_ is not None:
            self.format = pickle.loads(database.StringToPickleBytes(format_))

    def reload(self):
        BuildPath(path=self.path)

        self.info = self.database.BinJsonReader(self.path + self.database.INFO_FILE)

        self.name = self.info["name"]
        format_ = self.info["format"]
        self.format = None
        if format_ is not None:
            self.format = pickle.loads(self.database.StringToPickleBytes(format_))

    def set_format(self, format_: NameList): ...

    def __eq__(self, other):
        if not isinstance(other, ABCStore):
            return False
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)


class ABCDataBase(ABC):
    INFO_FILE = "INFO.BinJson"
    DATA_FILE = "DATA.BinData"
    HISTORY_FILE = "HISTORY.BinHistory"
    LOG_File = "Log.BinLog"

    name: str
    path: str
    stores: set[ABCStore]
    Store: Type[ABCStore]

    def __init__(self, __name: str, __path: str) -> None:
        self.name = __name

    def store_path(self, __store_name: str):
        return f"{self.path}{__store_name}\\"

    def _DBPathFinder(self) -> set:
        dirs = {dir_name for dir_name in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, dir_name))}

        paths = set()
        for dir_ in dirs:
            try:
                path = self.store_path(dir_)
                open(path + self.INFO_FILE, mode='rb').close()
                paths.add(path)
            except FileNotFoundError:
                pass
        return paths

    def create(self, __store_name: str) -> None:
        raise AttributeError

    def log(self, msg: str, operator: str) -> None:
        raise AttributeError

    @staticmethod
    def BinJsonReader(__file_path: str):
        with open(__file_path, mode="rb") as file:
            data = json.loads(file.read().decode("utf-8"))
        return data

    @staticmethod
    def BinJsonWriter(__file_path: str, obj) -> None:
        data = json.dumps(obj)
        with open(__file_path, "wb") as file:
            file.write(data.encode("utf-8"))

    def BinJsonChanger(self, __file_path: str, path: tuple[str], value: Union[str, bytes]):
        json_obj = ABCDataBase.BinJsonReader(__file_path)
        if type(value) is bytes:
            value = self.PickleBytesToString(value)
        obj = json_obj
        for p in path[:-1]:
            obj = json_obj.__getitem__(p)
        obj.__setitem__(path[-1], value)
        ABCDataBase.BinJsonWriter(__file_path, json_obj)

    @staticmethod
    def PickleBytesToString(byte: bytes):
        return byte.decode("unicode_escape")

    @staticmethod
    def StringToPickleBytes(string: str):
        return string.encode("utf-8", "unicode_escape").replace(b'\xc2', b'')

    def __getitem__(self, item) -> ABCStore:
        ...


class ABCServer(ABC):
    name: str
    path: str
    file: Union[TextIO, BinaryIO]

    DataBase: Type[ABCDataBase]
    DBs: set[ABCDataBase]

    USERDATA_FILE: str = "Users.json"

    def _file_input_loop(self) -> None:
        """
        运行时逐行读取并执行流
        """

    def _serve(self, conn: SocketIo, name: str) -> None:
        """
        对客户端的服务方法 (在线程中)
        :param conn: 连接到的客户端套接字对象
        :param name: 线程名称
        """

    def _recv_loop(self) -> None:
        """
        接受客户端套接字连接请求的循环 (在线程中)
        """

    def log(self, msg: str, level: int) -> None:
        """
        以指定格式输出日志
        :param msg: 日志消息
        :param level: 日志等级
        """

    def _start_thread(self) -> None:
        """
        用于启动线程
        """

    def start(self) -> None:
        """
        启动数据库服务器
        """

    def stop(self) -> None:
        """
        停止数据库服务器
        """

    def restart(self) -> None:
        """
        重启数据库服务器
        """

    def join(self, timeout=None) -> None:
        """
        等待服务器完全关闭
        :param timeout: 超时时间
        """

    def bind(self, __address: Union[tuple[any, ...], str, bytes]) -> None:
        """
        绑定数据库服务器
        :param __address: 绑定到的ip及端口
        """

    def listen(self, __backlog: int) -> None:
        """
        :param __backlog: 最大连接等待数
        """

    def is_alive(self) -> bool:
        """
        检查服务器是否开启
        """

    def __getitem__(self, item) -> ABCDataBase:
        raise AttributeError


class Event(ABC):
    raw: str

    def __str__(self) -> str:
        """
        :return: 事件名
        """
        return self.raw

    def __repr__(self) -> str:
        """
        :return: 事件名
        """
        return self.raw

    def __eq__(self, other) -> bool:
        """
        :param other: 另一个事件
        :return: 是否相等
        """
        return self.raw == str(other)

    def __hash__(self) -> int:
        """
        :return: 哈希值
        """
        return hash(self.raw)

    def func(self, server: ABCServer, **_kwargs):
        """
        :param server: 数据库服务器
        """


def MKEvent(name: str) -> Event:
    event = Event()
    event.raw = name
    return event


class RunSuccess(Event):
    raw = "RUN_SUCCESS"

    def __str__(self):
        return self.raw

    def __repr__(self):
        return self.raw

    def __eq__(self, other):
        return any((self.raw == str(other), isinstance(other, type(self))))


def BuildPath(path: str):
    path_list = path.split('\\')
    try:
        path_list.remove('')
    except ValueError:
        pass

    temp = ""

    for part in path_list:
        temp += part + '\\'
        try:
            os.mkdir(temp[:-1])
        except FileExistsError:
            pass
