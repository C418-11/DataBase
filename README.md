# DataBase

中/英 CN/EN

纯Python实现的数据库

Database implemented in pure Python

## 示例 / Example
    from database.DataBase import main
    
    if __name__ == '__main__':
        main()
    

## 输出 / Output
    DataBase 0.0.0.3
    (DEBUG) [2023-05-07 22:44:09]: DefaultDataBaseServer :: Init name=DefaultDataBaseServer path=.\DataBases\DefaultDataBaseServer\
    (INFO) [2023-05-07 22:44:09]: DefaultDataBaseServer :: Bind address=('127.0.0.1', 12345)
    (DEBUG) [2023-05-07 22:44:09]: DefaultDataBaseServer :: Listen backlog=1
    (INFO) [2023-05-07 22:44:09]: DefaultDataBaseServer :: Start!
    (DEBUG) [2023-05-07 22:44:09]: DefaultDataBaseServer :: Enter RecvLoop
    (DEBUG) [2023-05-07 22:44:09]: DefaultDataBaseServer :: Enter File Input
    (INFO) [2023-05-07 22:44:09]: DefaultDataBaseServer :: Received a new connect request socket=('127.0.0.1', 63069)
    (INFO) [2023-05-07 22:44:09]: DefaultDataBaseServer :: Serve-1 Serve Start! name=Serve-1 conn=('127.0.0.1', 63069)
    LOGIN.ASK_USER_AND_PASSWORD
    (INFO) [2023-05-07 22:44:10]: DefaultDataBaseServer :: default Try Login username=default password=default
    (INFO) [2023-05-07 22:44:10]: DefaultDataBaseServer :: default Success Login username=default info={'password': 'default'}
    LOGIN.LOGIN_SUCCESS
    (INFO) [2023-05-07 22:44:11]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=DATABASE.INIT
    EVENT.RUN_SUCCESS
    (INFO) [2023-05-07 22:44:12]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.CREATE_STORE
    EVENT.RUN_SUCCESS
    (INFO) [2023-05-07 22:44:14]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.SET_STORE_FORMAT
    EVENT.RUN_SUCCESS
    (INFO) [2023-05-07 22:44:15]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.SET_HISTORY_FORMAT
    EVENT.RUN_SUCCESS
    (INFO) [2023-05-07 22:44:16]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.APPEND
    EVENT.RUN_SUCCESS
    (INFO) [2023-05-07 22:44:17]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.GET_LINE
    {'a': 1, 'b': 2}
    (INFO) [2023-05-07 22:44:18]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.SET_LINE
    EVENT.RUN_SUCCESS
    (INFO) [2023-05-07 22:44:19]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.GET_LINE
    {'a': 11, 'b': 22}
    (INFO) [2023-05-07 22:44:21]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.DEL_LINE
    EVENT.RUN_SUCCESS
    (INFO) [2023-05-07 22:44:21]: DefaultDataBaseServer :: Stop!
    (INFO) [2023-05-07 22:44:22]: DefaultDataBaseServer :: Serve-1 Serve End! conn=('127.0.0.1', 63069)
    (DEBUG) [2023-05-07 22:44:29]: DefaultDataBaseServer :: Exit RecvLoop
    进程已结束,退出代码0

:D
