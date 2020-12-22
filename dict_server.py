from multiprocessing import Process
from socket import socket
from time import sleep

from dict_database import DictDatabase

#创建套接字，启动并发服务类
class DictServer:
    def __init__(self,host="",port=0):
        self.host = host
        self.port = port
        self.ADDR=(host,port)
        self.__tcp = self.__create_tcp()
    #创建套接字
    def __create_tcp(self):
        self.socket = socket()
        self.socket.bind(self.ADDR)
        return self.socket
    #创建并发进程
    def start(self):
        self.__tcp.listen(5)
        while 1:
            connfd,addr = self.__tcp.accept()
            print("Connect from",addr)
            p =DictProcess(connfd)
            p.start()

#创建进程类，循环接受客户端需求
class DictProcess(Process):
    def __init__(self,connfd):
        self.connfd=connfd
        self.handle = DictHandle(connfd)
        super().__init__(daemon= True)

    def run(self):
        db.cu()
        while 1:
            data = self.connfd.recv(1024)
            if not data and data == b"E":
                break
            self.handle.request(data)
        db.cur.close()
        self.connfd.close()

#逻辑处理类
class DictHandle:
    def __init__(self,connfd):
        self.connfd = connfd

    def request(self,data):
        msg = data.decode().split(" ",2)
        if msg[0] == "R":
            self.do_register(msg[1],msg[2])
        elif msg[0] == "L":
            self.do_login(msg[1],msg[2])
        elif msg[0] == "Q":
            self.do_query(msg[1],msg[2])
        elif msg[0] == "H":
            self.do_history(msg[1])

    def do_register(self, name,pwd):
        if db.register_user(name,pwd):
            self.connfd.send(b"ok")
        else:
            self.connfd.send(b"no")

    def do_login(self,name,pwd):
        if db.login_user(name,pwd):
            self.connfd.send(b"ok")
        else:
            self.connfd.send(b"no")

    def do_query(self, name, word):
        mean = db.query_word(name,word)
        msg = word +":"+ mean
        self.connfd.send(msg.encode())

    def do_history(self, name):
        foot = db.history(name)
        for data in foot:
            msg = "%d  %s   %s   %s" % data
            self.connfd.send(msg.encode())
            sleep(0.01)
        self.connfd.send(b"##")

if __name__ == '__main__':
    d = DictServer("0.0.0.0",33333)
    db = DictDatabase()
    d.start()
