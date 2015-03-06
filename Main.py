# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Main.py
# Description :    程序的主要内容就在该类中的Main方法
# Author      :    Frank
# Date        :    2014.03.04
# ######################################################

from Init import *

class Zhihu2ebook(object):
    def __init__(self):
        u"""
        ContentList.txt存放需要爬取的地址（可能是收藏夹地址，可能是某用户的地址）
        ContentList.txt使用$符号区隔开，同一行内的链接信息会放在一本电子书中
        :return: TODO
        """
        self.checkUpdate()   # 检查是否需要更新，如果有更新，默认浏览器打开链接
        init = Init()
        self.conn = init.getConn()
        self.epubContent = {}
        self.epubInfolist = []
        self.baseDir = os.path.realpath('.')  # 获得当前目录的绝对路径



    def checkupdate(self):
        u"""
        TODO：
        利用网络上某个文件的内容（时间对比）检查是否需要更新，如果时间信息是新的，
        自动用默认浏览器打开连接，（打算将最新版本链接置为百度网盘链接）
        :return:
        """
        print u"检查是否有新版本..."
