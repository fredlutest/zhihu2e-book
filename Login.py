# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Login.py
# Description :    用于登陆的类
# Author      :    Frank
# Date        :    2014.03.04
# ######################################################

import datetime

from Setting import *
from BaseClass import *

class Login(BaseClass, HttpBaseClass, SqlClass, CookieBaseClass):
    """
    用于登陆网站的类
    """
    def __init__(self, conn):
        self.setting = Setting()

    def send_message(self, account, password, captcha = ''):
        pass
