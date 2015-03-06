# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Init.py
# Description :    用于程序运行前的初始化
# Author      :    Frank
# Date        :    2014.03.04
# ######################################################

import os

class Init(object):
    def __init__(self):
        """
        用于程序的初始化操作
        初始化数据库，得到操作数据库的cursor对象
        :return:
        """
        # TODO
        self.initDB()

    def getConn(self):
        """
        返回数据库连接的connect
        :return:
        """
        # TODO
        # return self.conn
        return

    def getCursor(self):
        """
        返回数据库连接的cursor（游标）
        :return:
        """
        # return self.cursor
        return


    def initDB(self):
        dbFile = r'./zhihuDB.db'
        return