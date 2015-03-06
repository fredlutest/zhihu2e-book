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
        self.initDB()


    def initDB(self):
        dbFile = r'./zhihuDB.db'
        return