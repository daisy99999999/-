import sys
from socket import socket

class ClientView:
    def __init__(self):
        self.controll = ClientControll()

    def meau(self):
        while 1:
            print("**************首  页***************")
            print("1)登录         2)注册         3)退出 ")
            print("***********************************")
            msg = input("请输入选项")
            if msg == "1":
                name = self.controll.login()
                self.meau_2(name)
            elif msg == "2":
                name = self.controll.register()
                self.meau_2(name)
            elif msg == "3":
                self.controll.exit()
                sys.exit("谢谢使用")
            else:
                print("请重新输入选项")

    def meau_2(self,name):
        while 1 :
            print("****************菜  单*******************")
            print("1)查询单词       2)查询浏览记录      3)注销 ")
            print("****************************************")
            msg = input("请输入选项")
            if msg == "1":
                self.controll.query(name)
            elif msg == "2":
                self.controll.history(name)
            elif msg == "3":
                self.controll.exit()
                sys.exit("谢谢使用")
            else:
                print("请重新输入选项")

    def main(self):
        self.meau()

class ClientControll:
    def __init__(self):
        self.ADDR = ("176.50.2.30",33333)
        self.tcp = socket()
        self.tcp.connect(self.ADDR)

    def register(self):
        while 1:
            name = input("请输入用户名")
            pwd = input("请输入密码")
            if " " in name or " " in pwd:
                print("用户名和密码不能有空格")
                continue
            msg = "R " + name + " " + pwd
            self.tcp.send(msg.encode())
            data = self.tcp.recv(128)
            if data == b"ok":
                print("注册成功")
                return name
            else:
                print("用户名重复请重新注册")

    def login(self):
        while 1:
            name = input("请输入用户名")
            pwd = input("请输入密码")
            msg = "L " + name + " " + pwd
            self.tcp.send(msg.encode())
            data = self.tcp.recv(128)
            if data == b"ok":
                print("登录成功")
                return name
            else:
                print("用户名或者密码输入错误")

    def exit(self):
        self.tcp.send(b"E")
        self.tcp.close()

    def query(self,name):
        while 1:
            word = input("请输入要查询的单词：")
            if word == "##":
                break
            data = "Q " + name + " " + word
            self.tcp.send(data.encode())
            mean = self.tcp.recv(1024*10)
            print(mean.decode())

    def history(self,name):
        data = "H "+ name
        self.tcp.send(data.encode())
        while 1:
            foot = self.tcp.recv(1024)
            if foot == b"##":
                break
            print(foot.decode())

if __name__ == '__main__':
    cv = ClientView()
    cv.main()