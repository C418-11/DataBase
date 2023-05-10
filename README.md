# DataBase

中/英 CN/EN

纯Python实现的数据库

Database implemented in pure Python

##### 警告/ WARN
    此文件仅适配与0.0.0.3b版
    This file is only compatible with version 0.0.0.3b
    
    已落后于已上传版本
    Has fallen behind the uploaded version
    
    请以源代码为准
    Please refer to the source code for accuracy
    

### 示例 / Example
    from database.DataBase import main
    
    if __name__ == '__main__':
        main()
    

### 服务器输出 / ServerOutput
    (DEBUG) [2023-05-08 23:08:36]: DefaultDataBaseServer :: Init name=DefaultDataBaseServer path=.\DataBases\DefaultDataBaseServer\
    (INFO) [2023-05-08 23:08:36]: DefaultDataBaseServer :: Bind address=('127.0.0.1', 12345)
    (DEBUG) [2023-05-08 23:08:36]: DefaultDataBaseServer :: Listen backlog=1
    (INFO) [2023-05-08 23:08:36]: DefaultDataBaseServer :: Start!
    (DEBUG) [2023-05-08 23:08:36]: DefaultDataBaseServer :: Enter RecvLoop
    (DEBUG) [2023-05-08 23:08:36]: DefaultDataBaseServer :: Enter File Input
    (INFO) [2023-05-08 23:08:36]: DefaultDataBaseServer :: Received a new connect request socket=('127.0.0.1', 51692)
    (INFO) [2023-05-08 23:08:36]: DefaultDataBaseServer :: Serve-1 Serve Start! name=Serve-1 conn=('127.0.0.1', 51692)
    (INFO) [2023-05-08 23:08:37]: DefaultDataBaseServer :: default Try Login username=default password=default
    (INFO) [2023-05-08 23:08:37]: DefaultDataBaseServer :: default Success Login username=default info={'password': 'default'}
    (INFO) [2023-05-08 23:08:38]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=DATABASE.INIT
    (INFO) [2023-05-08 23:08:39]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.CREATE_STORE
    (INFO) [2023-05-08 23:08:41]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.SET_STORE_FORMAT
    (INFO) [2023-05-08 23:08:42]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.SET_HISTORY_FORMAT
    (INFO) [2023-05-08 23:08:43]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.APPEND
    (INFO) [2023-05-08 23:08:44]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.GET_LINE
    (INFO) [2023-05-08 23:08:45]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.SET_LINE
    (INFO) [2023-05-08 23:08:47]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.GET_LINE
    (INFO) [2023-05-08 23:08:48]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.DEL_LINE
    (INFO) [2023-05-08 23:08:49]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=LOGIN.ACK_USER_AND_PASSWORD
    (INFO) [2023-05-08 23:08:49]: DefaultDataBaseServer :: default Try Login username=default password=default
    (INFO) [2023-05-08 23:08:49]: DefaultDataBaseServer :: default Success Login username=default info={'password': 'default'}
    (INFO) [2023-05-08 23:08:50]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=DATABASE.INIT
    (INFO) [2023-05-08 23:08:51]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.CREATE_STORE
    (INFO) [2023-05-08 23:08:52]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.SET_STORE_FORMAT
    (INFO) [2023-05-08 23:08:55]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.SET_HISTORY_FORMAT
    (INFO) [2023-05-08 23:08:56]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.APPEND
    (INFO) [2023-05-08 23:08:57]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.GET_LINE
    (INFO) [2023-05-08 23:08:58]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.SET_LINE
    (INFO) [2023-05-08 23:08:59]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.GET_LINE
    (INFO) [2023-05-08 23:09:01]: DefaultDataBaseServer :: Serve-1 Received a new event request! event=STORE.DEL_LINE
    (INFO) [2023-05-08 23:09:02]: DefaultDataBaseServer :: Serve-1 Lost Connect! reason=SOCKET.CONNECT_CLOSE
    (INFO) [2023-05-08 23:09:02]: DefaultDataBaseServer :: Serve-1 Serve End! conn=('127.0.0.1', 51692)
    (INFO) [2023-05-08 23:09:03]: DefaultDataBaseServer :: Stop!
    (DEBUG) [2023-05-08 23:09:07]: DefaultDataBaseServer :: Exit RecvLoop
    
### 客户端输出 / ClientOutput
    
    LOGIN.ASK_USER_AND_PASSWORD
    LOGIN.LOGIN_SUCCESS
    EVENT.RUN_SUCCESS
    EVENT.RUN_SUCCESS
    EVENT.RUN_SUCCESS
    EVENT.RUN_SUCCESS
    EVENT.RUN_SUCCESS
    {'a': 1, 'b': 2}
    EVENT.RUN_SUCCESS
    {'a': 11, 'b': 22}
    EVENT.RUN_SUCCESS
    <database.Event.LOGIN.AckUserAndPassword object at 0x000001FF7F9C3F40> LOGIN.LOGIN_SUCCESS
    <database.Event.DATABASE.InitDataBase object at 0x000001FF7FA082E0> EVENT.RUN_SUCCESS
    <database.Event.STORE.CreateStore object at 0x000001FF7FA08340> EVENT.RUN_SUCCESS
    <database.Event.STORE.SetStoreFormat object at 0x000001FF7FA08400> EVENT.RUN_SUCCESS
    <database.Event.STORE.SetHistoryFormat object at 0x000001FF7FA08460> EVENT.RUN_SUCCESS
    <database.Event.STORE.Append object at 0x000001FF7FA08520> EVENT.RUN_SUCCESS
    <database.Event.STORE.GetLine object at 0x000001FF7FA08580> {'a': 1, 'b': 2}
    <database.Event.STORE.SetLine object at 0x000001FF7FA08640> EVENT.RUN_SUCCESS
    <database.Event.STORE.GetLine object at 0x000001FF7FA086A0> {'a': 11, 'b': 22}
    <database.Event.STORE.DelLine object at 0x000001FF7FA08700> EVENT.RUN_SUCCESS

:D
