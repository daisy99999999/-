import pymysql

class DictDatabase:
        database_args = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "123456",
            "database": "dict",
            "charset": "utf8"}

        def __init__(self):
            self.db = pymysql.connect(**DictDatabase.database_args)

        def cu(self):
            self.cur = self.db.cursor()

        def close(self):
            # self.cur.close()
            self.db.close()

   # 查询单词解释方法
        def query_word(self,name,word):
            sql = "insert into history(word,user_name) values(%s,%s);"
            self.cur.execute(sql, [word, name])
            self.db.commit()
            sql = "select mean from words where word=%s;"
            self.cur.execute(sql,[word])
            # 查到：(mean,)  没查到：None
            mean = self.cur.fetchone()
            if mean:
                return mean[0]
            else:
                return "Not Found"

        def history(self,name):
            sql = "select * from history where user_name = %s order by times desc limit 10 ;"
            self.cur.execute(sql,[name])
            foot = self.cur.fetchall()
            return foot

        def register_user(self,name,pwd):
            sql = "insert into users(name,pwd) values(%s,%s);"
            try:
                self.cur.execute(sql,[name,pwd])
                self.db.commit()
                return True
            except:
                self.db.rollback()
                return False

        def login_user(self,name,pwd):
            sql = "select pwd from users where name=%s;"
            self.cur.execute(sql, [name])
            password = self.cur.fetchone()
            if pwd == password[0]:
                return True
            else:
                return False