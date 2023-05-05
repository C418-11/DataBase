# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"

from database.ABC import ABCServer
from database.ABC import Event
from database.ABC import MKEvent
from database.ABC import RunSuccess
from database._def_event import *

STOP = MKEvent("STOP")
RESTART = MKEvent("RESTART")

ASK_USER_AND_PASSWORD = MKEvent("ASK_USER_AND_PASSWORD")
ASK_USER_AND_PASSWORD_TIMEOUT = MKEvent("ASK_USER_AND_PASSWORD_TIMEOUT")

ACK_USER_AND_PASSWORD = AckUserAndPassword

RUN_SUCCESS = RunSuccess()

LOGIN_TIMEOUT = MKEvent("LOGIN_TIMEOUT")
USER_NOT_FIND = USER_NOT_FIND
WRONG_PASSWORD = WRONG_PASSWORD
LOGIN_SUCCESS = LOGIN_SUCCESS

EVENT_NOT_FIND = MKEvent("EVENT_NOT_FIND")

CONNECT_CLOSE = MKEvent("CONNECT_CLOSE")

REG_USER = RegUser
RESET_PASSWORD = ReSetPassword
DEL_USER = DelUser

INIT_DATABASE = InitDataBase
CREATE_DATABASE = CreateDataBase
SET_DATABASE_FORMAT = SetDataBaseFormat

DEBUG_EVENT = DebugEvent

__event_to_func = {
    ACK_USER_AND_PASSWORD.raw: AckUserAndPassword.func,
    DEBUG_EVENT.raw: DebugEvent.func,
    REG_USER.raw: RegUser.func,
    RESET_PASSWORD.raw: ReSetPassword.func,
    DEL_USER.raw: DelUser.func,
    INIT_DATABASE.raw: InitDataBase.func,
    CREATE_DATABASE.raw: CreateDataBase.func,
    SET_DATABASE_FORMAT.raw: SetDataBaseFormat.func
}


def EventToFunc(event: Event, server: ABCServer = None, run: bool = False, **kwargs):
    try:
        func = __event_to_func[event.raw]
    except KeyError:
        return EVENT_NOT_FIND
    if run:
        ret = func(self=event, server=server, **kwargs)
        if ret is None:
            ret = RUN_SUCCESS
        return ret
    return func


__all__ = (
    "EventToFunc",
    "STOP",
    "RESTART",
    "ASK_USER_AND_PASSWORD",
    "ASK_USER_AND_PASSWORD_TIMEOUT",
    "ACK_USER_AND_PASSWORD",
    "RUN_SUCCESS",
    "LOGIN_TIMEOUT",
    "USER_NOT_FIND",
    "WRONG_PASSWORD",
    "LOGIN_SUCCESS",
    "EVENT_NOT_FIND",
    "CONNECT_CLOSE",
    "REG_USER",
    "RESET_PASSWORD",
    "DEL_USER",
    "INIT_DATABASE",
    "CREATE_DATABASE",
    "SET_DATABASE_FORMAT",
    "DEBUG_EVENT"
)
