# -*- coding: utf-8 -*-

"""
May this file will help you to do st :D
"""
import pickle
import socket
import sys
import threading
import time
from collections import deque
from threading import Thread
from typing import BinaryIO
from typing import Type
from typing import TextIO
from typing import Union

from database import logging
from database.ABC import ABCDataBase
from database.ABC import ABCServer
from database.ABC import ABCStore
from database.ABC import BuildPath
from database.ABC import NameList
from database.Event import *
from database.Event.ABC import EVENT_NOT_FIND
from database.Event.ABC import Event
from database.Event.ABC import RunSuccess
from database.Event.ABC import RUN_FAILED
from database.Event.ABC import EventToFunc
from database.SocketIO import Address
from database.SocketIO import Server
from database.SocketIO import SocketIo
from database.logging import DEBUG
from database.logging import INFO
from database.logging import WARNING

PATH = ".\\DataBases\\"


class Store(ABCStore):
    database: ABCDataBase

    def __init__(self, __store_path: str, database: ABCDataBase):
        super().__init__(__store_path, database)

    def set_format(self, format_: NameList):
        if self.database.BinJsonReader(self.path + self.database.INFO_FILE)["format"] is not None:
            raise RuntimeError("Format has been set")
        self.database.BinJsonChanger(self.path + self.database.INFO_FILE, ("format",), pickle.dumps(format_))

        self.history("set_format", {"format": format_.ToDict()})
        self.save()

        self.reload()

    def append(self, line: NameList):
        self.data.append(line.ToDict())
        self.history("append", {"line": line.ToDict()})
        self.save()


class DataBase(ABCDataBase):
    def __init__(self, __name: str,
                 __path: str,
                 *,
                 time_format: str = "%Y-%m-%d %H:%M:%S",
                 log_format: str = "[{time}] (level): {store} :: {msg}",
                 log_mode: "a | w" = 'a'):
        super().__init__(__name, __path)

        path = PATH
        if PATH.endswith('\\'):
            path = PATH[:-1]

        self.path = '\\'.join((path, __path, __name, ''))
        self.log_path = self.path + self.LOG_File

        BuildPath(path=self.path)

        self.time_format = time_format
        self.log_format = log_format

        self.logging = logging.Logger(name=self.name, stream=open(self.log_path, f"{log_mode}b"))
        self.logging.type = bytes
        self.logging: logging.Logger
        self.Store = Store

        self.stores = set()
        for store_path in self._DBPathFinder():
            try:
                self.stores.add(self.Store(store_path, self))
            except Exception as err:
                self.log(msg=f"An error was raised while loading Store store_path={store_path} err={err}", level=WARNING)

    def create(self, __store_name: str):
        store_path = self.store_path(__store_name)

        id_ = time.time()

        try:
            info = self.BinJsonReader(store_path + DataBase.INFO_FILE)
            id_ = info["id"]
        except FileNotFoundError:
            pass
        except KeyError:
            pass

        BuildPath(path=store_path)

        self.BinJsonWriter(
            store_path + self.INFO_FILE,
            {
                "id": str(id_),
                "name": __store_name,
                "format": None,
                "history_format": "[{time_}]({type_}): {value}"
            }
        )
        self.BinJsonCreate(
            store_path + self.DATA_FILE,
            []
        )
        self.BinJsonCreate(
            store_path + self.HISTORY_FILE,
            []
        )

        self.stores.add(self.Store(store_path, self))

    def log(self, msg: str, level, store: str = "SYSTEM"):
        time_ = time.strftime(self.time_format, time.localtime())
        message = self.log_format.format(time=time_, level=level, store=store, msg=msg)

        bin_msg = message.encode(encoding="utf-8", errors="replace")

        self.logging.bin_log(msg=bin_msg, level=level)

    def __getitem__(self, item):
        for st in self.stores:
            if st.name == item:
                return st


class DataBaseServer(ABCServer):
    """
    DataBase Server
    """

    def __init__(self,
                 name: str = "DefaultDataBaseServer",
                 path: str = PATH,
                 init_socket: tuple = None,
                 file: BinaryIO = sys.stdin,
                 database: Type[ABCDataBase] = DataBase,
                 *,
                 debug: bool = False,
                 time_format: str = "%Y-%m-%d %H:%M:%S",
                 disable_log: bool = False,
                 log_file: TextIO = sys.stderr,
                 log_level: int = WARNING,
                 log_format: str = "({level}) [{time}]: {server} :: {msg}"):
        """
        :param name: 数据库名称
        :param path: 数据库位置文件夹
        :param init_socket: 数据库的网络套接字初始化参数
        :param file: 运行时需逐行读取并执行的流
        :param database: 指定数据库类型

        :param debug: 是否开启调试模式
        :param time_format: 时间格式化模板
        :param disable_log: 是否禁止记录日志
        :param log_file: 日志文件
        :param log_level: 最低日志输出等级
        :param log_format: 日志格式化模板
        """

        self.name = name
        self.path = path + name + "\\"
        self.file = file
        self.database = database

        self.debug = debug

        BuildPath(path=self.path)

        self.time_format = time_format

        self.logging = logging.Logger(name=name, level=log_level, stream=log_file)
        self.logging.disabled = disable_log
        self.log_format = log_format

        self.log(msg=f"Init name={self.name} path={self.path}", level=DEBUG)

        if init_socket is None:
            init_socket = (socket.AF_INET, socket.SOCK_STREAM)
        self.init_socket = init_socket
        self.server = Server(socket.socket(*self.init_socket))

        self.running = False
        self.cont_serve = 0
        self.recv_thread = Thread(target=self._recv_loop, name=self.name + "'s RecvLoop", daemon=True)
        self.file_input_thread = Thread(target=self._file_input_loop, name=self.name + "'s File Input", daemon=True)

        self.DBs = set()

    def _EventRunnerMaker(self, *, name: str = None):
        rollback_stack = deque(maxlen=64)

        if name is not None:
            name += ' '
        else:
            name = ''

        def Runner(event: Event):
            nonlocal self
            nonlocal rollback_stack
            nonlocal name

            rollback_stack.append(event)

            try:
                return_code = EventToFunc(event, self, True)
            except Exception as err:
                self.log(msg=f"{name}An error occurred while executing the event request! err_type={type(err)} err={err}", level=WARNING)
                rollback_stack.pop()
                if self.debug:
                    raise
                return RUN_FAILED

            if return_code == EVENT_NOT_FIND:
                self.log(msg=f"{name}An undefined event was requested! event={event}", level=INFO)
                rollback_stack.pop()
            elif not (isinstance(return_code, RunSuccess) or type(return_code) in (int, bool, str, list, bytes, tuple, dict, set)):
                self.log(msg=f"{name}Event request may fail to execute! return_code={return_code}", level=INFO)

            return return_code

        return Runner

    def _file_input_loop(self):
        self.log(msg="Enter File Input", level=DEBUG)

        _EventRunner = self._EventRunnerMaker()

        while self.running:
            line = self.file.readline()
            line = line.replace('\n', '')
            self.log(msg=f"A new line was read from the stream line={line}", level=DEBUG)
            if line == SERVER.STOP:
                self.stop()
                self.join()
                break

            if line == SERVER.RESTART:
                Thread(target=self.restart, name=self.name + "'s RESTART", daemon=True).start()
                break

            try:
                ret = eval(line)
                self.log(msg=f"A new line was executed from the stream ret_code={ret}", level=INFO)
            except Exception as err:
                self.log(f"An error was thrown while running a line in the flow err_type={type(err)} err={err}", level=WARNING)

        self.log(msg="Exit File Input", level=DEBUG)

    def _serve(self, conn: SocketIo, name: str):
        conn_peer_name = conn.cSocket.getpeername()
        self.log(msg=f"{name} Serve Start! name={name} conn={conn_peer_name}", level=INFO)

        conn.start_recv()
        conn.send(LOGIN.ASK_USER_AND_PASSWORD)

        ret_login = LOGIN.ASK_USER_AND_PASSWORD_TIMEOUT

        try:
            login = conn.recv(5)
            ret_login = EventToFunc(login, self, True)

            conn.send(ret_login)
            if ret_login != LOGIN.LOGIN_SUCCESS:
                self.log(msg=f"{name} Lost Connect! reason={ret_login}", level=WARNING)
                conn.close()

        except TimeoutError:
            conn.send(LOGIN.ASK_USER_AND_PASSWORD_TIMEOUT)
            self.log(msg=f"{name} Lost Connect! reason={LOGIN.ASK_USER_AND_PASSWORD_TIMEOUT}", level=WARNING)

        event_runner = self._EventRunnerMaker(name=name)

        while self.running and ret_login == LOGIN.LOGIN_SUCCESS:
            try:
                event = conn.recv(1)
                event: Event
                self.log(msg=f"{name} Received a new event request! event={event}", level=INFO)
            except TimeoutError:
                continue
            except threading.ThreadError:
                self.log(msg=f"{name} Lost Connect! reason={SOCKET.CONNECT_CLOSE}", level=INFO)
                break

            return_code = event_runner(event)

            try:
                conn.send(str(return_code))
            except ConnectionResetError:
                self.log(msg=f"{name} Lost Connect! reason={SOCKET.CONNECT_CLOSE}", level=INFO)
                break
            except OSError:
                self.log(msg=f"{name} Lost Connect! reason={SOCKET.CONNECT_CLOSE}", level=INFO)
                break

        self.log(msg=f"{name} Serve End! conn={conn_peer_name}", level=INFO)
        conn.close()

    def _recv_loop(self):
        self.log(msg=f"Enter RecvLoop", level=DEBUG)

        cont = 0

        while self.running:
            try:
                c_socket = self.server.get(10)[0]
                c_socket: SOCKET.socket
            except TimeoutError:
                continue
            except threading.ThreadError:
                raise
            self.log(msg=f"Received a new connect request socket={c_socket.getpeername()}", level=INFO)
            conn = SocketIo(c_socket)

            cont += 1
            thread_name = f"Serve-{cont}"

            Thread(target=self._serve, kwargs={"conn": conn, "name": thread_name}, daemon=True, name=thread_name).start()

        self.log(msg=f"Exit RecvLoop", level=DEBUG)

    def log(self, msg, level):
        level_name = logging.getLevelName(level=level)
        time_ = time.strftime(self.time_format, time.localtime())

        message = self.log_format.format(time=time_, level=level_name, server=self.name, msg=msg)

        self.logging.log(level=level, msg=message)  # 输出日志

    def _start_thread(self):
        try:
            self.recv_thread.start()
        except RuntimeError:
            self.recv_thread.join(10)
            self.recv_thread = Thread(target=self._recv_loop, name=self.name + "'s RecvLoop", daemon=True)
            self.recv_thread.start()
        try:
            self.file_input_thread.start()
        except RuntimeError:
            self.file_input_thread.join(10)
            self.file_input_thread = Thread(target=self._file_input_loop, name=self.name + "'s File Input", daemon=True)
            self.file_input_thread.start()

    def start(self):
        self.log(msg=f"Start!", level=INFO)
        self.running = True
        self.server.start()

        self._start_thread()

    def stop(self):
        self.log(msg=f"Stop!", level=INFO)
        self.running = False
        self.server.stop()
        self.server.join(10)

    def restart(self):
        self.log(msg=f"ReStart!", level=INFO)
        self.stop()
        self.join(10)
        self.server.restart(self.init_socket)
        self.start()

    def join(self, timeout=None):
        self.recv_thread.join(timeout=timeout)

    def bind(self, __address: Union[tuple[any, ...], str, bytes]):
        self.log(msg=f"Bind address={__address}", level=INFO)
        self.server.bind(__address)

    def listen(self, __backlog: int):
        self.log(msg=f"Listen backlog={__backlog}", level=DEBUG)
        self.server.listen(__backlog)

    def is_alive(self):
        return self.running

    def __getitem__(self, item):
        for db in self.DBs:
            if db.name == item:
                return db


def mv_client():
    c = SocketIo(Address("127.0.0.1", 12345))
    c.start_recv()
    print(c.recv(10))

    db_and_store = ("TestDB", "Store")

    event_to_run = [
        LOGIN.ACK_USER_AND_PASSWORD("default", "default"),
        DATABASE.INIT(db_and_store[0]),
        STORE.CREATE(*db_and_store),
        STORE.SET_FORMAT(*db_and_store, NameList("a", "b")),
        STORE.SET_HISTORY_FORMANT(*db_and_store, "[{time_}]({type_}): {value}"),
        STORE.APPEND(*db_and_store, NameList(a=1, b=2)),
        STORE.GET_LINE(*db_and_store, 0),
        STORE.SET_LINE(*db_and_store, 0, NameList(a=11, b=22)),
        STORE.GET_LINE(*db_and_store, 0),
        STORE.DEL_LINE(*db_and_store, 0)
    ]

    for event in event_to_run:
        try:
            c.send(event)
            print(c.recv(10))
        except Exception as err:
            print(err)

    c.close()


def main():
    s = DataBaseServer(log_level=DEBUG, debug=True)  # ,
    # log_file=open(PATH + "lasted.log", encoding='utf-8', mode='aw'))

    s.bind(("127.0.0.1", 12345))
    s.listen(1)
    s.start()

    mv_client()

    # time.sleep(10000)

    s.stop()
    s.join()


if __name__ == '__main__':
    # main()
    pass
