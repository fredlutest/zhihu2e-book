# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Login.py
# Description :    用于登陆的类
# Author      :    Frank
# Date        :    2014.03.04
# ######################################################

import datetime
import re

from Setting import *
from BaseClass import *

class Login(BaseClass, HttpBaseClass, SqlClass, CookieBaseClass):
    """
    用于登陆网站的类
    """
    def __init__(self, conn):
        self.setting = Setting()

    def send_message(self, account, password, captcha=''):
        xsrf = self.getXsrf(self.get_http_content())
        if xsrf == '':
            print u'知乎网页打开失败'
            print u'回车重新发送登陆请求'
            return False
        _xsrf = xsrf.split('=')[1]

    def getXsrf(self, content=''):
        u"""
        不清楚这个方法的作用
        提取xsrf信息
        """
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
        if xsrf == None:
            return ''
        else:
            return '_xsrf=' + xsrf.group(0)