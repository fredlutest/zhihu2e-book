# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Setting.py
# Description :    一些进行设置的函数，有print输出内容
# Author      :    Frank
# Date        :    2014.03.04
# ######################################################

import sys
reload(sys)
# 设置系统默认的编码为utf8
sys.setdefaultencoding('utf8')

import ConfigParser

class Setting():
    u"""
    *   account
        *   用户名
    *   password
        *   密码
    *   rememberAccount
        *   是否保存账号密码
            *   0
            *   1
    *   maxThread
        *   最大线程数
    *   picQuality
        *   图片质量
            *   0 =>   无图
            *   1 => 普通图
            *   2 => 高清图
    *   以下内容为答案过滤标准，不提供修改接口，只能在设置文件中手工修改
    *   contentLength
        *   答案长度
    *   contentAgree
        *   答案赞同数
    *   answerOrderBy
        *   答案排序依据
            *   length
            *   agree
            *   update
            *   userDefine(自定义排序顺序，为GUI做准备)
    *   questionOrderBy
        *   问题排序依据
            *   answerCount
            *   agreeCount
            *   userDefine
    *   contentLength
        *   答案长度
    """
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()




