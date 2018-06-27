#!/usr/bin/python3
import sqlite3,os


#---------------------------------------------全局配置--------------------------------------------#


# path="hr.db"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, "hr.db")
#---------------------------------------------全局配置--------------------------------------------#

class Link_db:

    #初始化连接
    def __init__(self):
        self.__db = sqlite3.connect(path)
        self.__cursor = self.__db.cursor()


    #返回cursor，实际上并没有用到。
    def GetCursor(self):
        return self.__db.cursor()

    #执行查询的语句，返回多个元组组成的元组。若执行失败则返回bool类型的False
    def select(self,sql):
        try:
            print("haha")
            self.__cursor.execute(sql)
            data = self.__cursor.fetchall()
            return data
        except:
            print("Error: unable to fecth data with sql query: "+sql)
            return False
        # self.__cursor.execute(sql)
        # data = self.__cursor.fetchall()
        # return data

    # 执行更新的语句，返回改变了多少行，为int类型。若执行失败则返回bool类型的False
    def update(self,sql):
        # try:
        #     Affect=self.__cursor.execute(sql)
        #     self.__db.commit()
        #     return Affect
        # except:
        #     print("Error: unable to update data with sql query: "+sql)
        #     self.__db.rollback()
        #     return False
        print("haha")
        Affect = self.__cursor.execute(sql)
        self.__db.commit()
        return Affect

    #关闭连接
    def close(self):
        if(self.__db!=None):
            self.__db.close()

    #重新连接
    def reconnect(self):
        try:
            self.__db = sqlite3.connect(path)
            self.__cursor = self.__db.cursor()
        except:
            print("连接数据库失败")


