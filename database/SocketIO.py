# -*- coding: utf-8 -*-

import pickle
import socket
import sys
import threading
import time
import traceback
from collections import deque
from threading import Thread
from typing import IO
from typing import Union


class Address:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def get(self):
        return self.ip, self.port

    def __str__(self):
        return str(f"{self.ip}: {self.port}")

    def __repr__(self):
        return self.__str__()

    def __call__(self, *args, **kwargs):
        return self.get()


class Recv:
    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            self.data = deque()

    def put(self, obj: object):
        return self.data.append(obj)

    def get(self, timeout: Union[int, float] = float("inf")):
        start_time = time.time()

        try:
            return self.data.popleft()
        except IndexError:
            if timeout is None:
                raise

        float(timeout)

        delay = 0

        while (time.time() - start_time) <= timeout:
            try:
                return self.data.popleft()
            except IndexError:
                pass

            time.sleep(delay)

            if delay < 3:
                delay += 0.01

        raise TimeoutError("Timeout waiting for return value")

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return Recv(self.data.copy())

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return bool(self.data)

    def __iter__(self):
        return iter(self.data)


class SocketIo:
    def __init__(self, address: Union[Address, socket.socket], print_error: bool = True, err_file: IO = sys.stderr):

        """
        :param address: 绑定到的套接字
        :param print_error: 是否额外打印错误
        """

        if type(address) != Address:
            self.cSocket = address
        else:
            self.cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cSocket.connect(address.get())

        self.print_error = print_error
        self.err_file = err_file

        self.recv_queue = Recv()

        self.running = False
        self.recv_t = Thread(target=self._recv_loop, name="RecvThread", daemon=True)

    def _recv_all(self, max_size: int = 4096) -> bytes:
        size = int(self.cSocket.recv(max_size).decode())
        recv_size = 0

        recv_bytes = []

        while recv_size != size:
            temp_bytes = self.cSocket.recv(max(min(size - recv_size, max_size), 0))

            recv_size += temp_bytes.__sizeof__()
            recv_bytes.append(temp_bytes)

        return b''.join(recv_bytes)

    def _recv_loop(self):
        while self.running:
            try:
                byte = self._recv_all()
                self.recv_queue.put(pickle.loads(byte))
            except ConnectionResetError:
                self.cSocket.close()
                break
            except ConnectionAbortedError:
                self.cSocket.close()
                break
            except Exception as err:
                self.cSocket.close()
                if self.print_error:
                    traceback.print_exception(err, file=self.err_file)
                    break
                else:
                    raise

    def start_recv(self):
        self.running = True
        self.recv_t.start()
        return self.recv_t.is_alive()

    def recv(self, timeout: Union[int, float] = float("inf")):
        if not self.recv_t.is_alive():
            raise threading.ThreadError("Recv Thread is not alive!")

        return self.recv_queue.get(timeout=timeout)

    def get_que(self):
        return self.recv_queue

    def send(self, arg: any):
        byte = pickle.dumps(arg)
        size_of = str(byte.__sizeof__()).encode()
        self.cSocket.sendall(size_of)
        time.sleep(0.5)
        self.cSocket.sendall(byte)

    def close(self):
        self.cSocket.close()


class Server:
    """
    Sever of database
    """

    def __init__(self, s_socket: socket.socket):
        self._running = False
        self._s_socket = s_socket

        self._connect_request_pool = Recv()

        self._recv_connect_thread = Thread(target=self._recv_connect, name="RecvConnectThread", daemon=True)

        self._address = None
        self._backlog = None

    def _start_thread(self):
        try:
            self._recv_connect_thread.start()
        except RuntimeError:
            self._recv_connect_thread.join(10)
            self._recv_connect_thread = Thread(target=self._recv_connect, name="RecvConnectThread", daemon=True)
            self._recv_connect_thread.start()

    def _recv_connect(self):
        while self._running:
            try:
                connect = self._s_socket.accept()
            except OSError:
                break
            self._connect_request_pool.put(connect)

    def get(self, timeout: Union[int, float] = float("inf")):
        if not self._recv_connect_thread.is_alive():
            raise threading.ThreadError("Recv Connect Thread is not alive!")

        return self._connect_request_pool.get(timeout=timeout)

    def get_que(self):
        return self._connect_request_pool

    def start(self):
        self._running = True
        self._start_thread()

    def stop(self):
        self._running = False
        self._s_socket.close()

    def bind(self, __address: Union[tuple[any, ...], str, bytes]):
        self._address = __address
        self._s_socket.bind(self._address)

    def listen(self, __backlog: int):
        self._backlog = __backlog
        self._s_socket.listen(self._backlog)

    def is_alive(self):
        return self._recv_connect_thread.is_alive()

    def join(self, timeout=None):
        self._recv_connect_thread.join(timeout=timeout)

    def restart(self, init_socket: Union[tuple, socket.socket]):
        if type(init_socket) is tuple:
            self._s_socket = socket.socket(*init_socket)
        else:
            self._s_socket = init_socket

        if self._address is None:
            raise AttributeError("address not find")
        if self._backlog is None:
            raise AttributeError("backlog not find")
        self.bind(self._address)
        self.listen(self._backlog)
        self.start()


def main():
    pass


if __name__ == '__main__':
    main()
