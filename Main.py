# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Main.py
# Description :    程序的主要内容就在该类中的Main方法
# Author      :    Frank
# Date        :    2014.03.04
# ######################################################

class Zhihu2ebook(object):
    def __init__(self):
        u"""
        ContentList.txt存放需要爬取的地址（可能是收藏夹地址，可能是某用户的地址）
        ContentList.txt使用$符号区隔开，同一行内的链接信息会放在一本电子书中
        :return: TODO
        """


    def checkUpdate(self):
        u"""
        TODO：
        利用网络上某个文件的内容（时间对比）检查是否需要更新，如果时间信息是新的，
        自动用默认浏览器打开连接，（打算将最新版本链接置为百度网盘链接）
        :return:
        """
