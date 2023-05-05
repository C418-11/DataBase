# DataBase

中/英 CN/EN

纯Python实现的数据库

Database implemented in pure Python

## 示例 / Example
    from database.DataBase import main
    
    if __name__ == '__main__':
        main()
    

## 输出 / Output
    DataBase BT 0.0.0.2f
    (DEBUG) [2023-05-05 23:35:16]: DefaultDataBaseServer :: Init name=DefaultDataBaseServer path=.\DataBases\DefaultDataBaseServer\
    (INFO) [2023-05-05 23:35:16]: DefaultDataBaseServer :: Bind address=('127.0.0.1', 12345)
    (DEBUG) [2023-05-05 23:35:16]: DefaultDataBaseServer :: Listen backlog=1
    (INFO) [2023-05-05 23:35:16]: DefaultDataBaseServer :: Start!
    (DEBUG) [2023-05-05 23:35:16]: DefaultDataBaseServer :: Enter RecvLoop
    (DEBUG) [2023-05-05 23:35:16]: DefaultDataBaseServer :: Enter File Input
    (INFO) [2023-05-05 23:35:16]: DefaultDataBaseServer :: Received a new connect request socket=('127.0.0.1', 55128)
    (INFO) [2023-05-05 23:35:16]: DefaultDataBaseServer :: Serve-1 Serve Start! name=Serve-1 conn=('127.0.0.1', 55128)
    ASK_USER_AND_PASSWORD
    (INFO) [2023-05-05 23:35:17]: DefaultDataBaseServer :: default Try Login username=default password=default
    (INFO) [2023-05-05 23:35:17]: DefaultDataBaseServer :: default Success Login username=default info={'password': 'default'}
    LOGIN_SUCCESS
    (INFO) [2023-05-05 23:35:18]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=INIT_DATABASE
    RUN_SUCCESS
    (INFO) [2023-05-05 23:35:19]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=CREATE_DATABASE
    RUN_SUCCESS
    (INFO) [2023-05-05 23:35:21]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=SET_DATABASE_FORMAT
    RUN_SUCCESS
    (INFO) [2023-05-05 23:35:21]: DefaultDataBaseServer :: Stop!
    (INFO) [2023-05-05 23:35:22]: DefaultDataBaseServer :: Serve-1 Serve End! conn=('127.0.0.1', 55128)
    (DEBUG) [2023-05-05 23:35:26]: DefaultDataBaseServer :: Exit RecvLoop
    结束程序
    
    进程已结束,退出代码0

:D
