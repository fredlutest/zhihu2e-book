# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Setting.py
# Description :    一些进行设置的函数，有print输出内容
# Author      :    Frank
# Date        :    2014.03.04
# ######################################################

from baseclass import *

import ConfigParser
import os
import re

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
        # ConfigParser这个类能够很好地操作ini格式的文件（配置文件，保存一些重要的配置信息）
        self.config = ConfigParser.SafeConfigParser()
        self.settingList = [
            'account',
            'password',
            'rememberAccount',
            'maxThread',
            'picQuality',
            'contentLength',
            'contentAgree',
            'answerOrderBy',
            'questionOrderBy'
        ]
        self.setDict = {
            'account': 'mengqingxue2014@qq.com',  # TODO 有空注册一个163邮箱
            'password': '131724qingxue',
            'rememberAccount': '0',
            'maxThread': '18',
            'picQuality': '0',
            'contentLength': '0',
            'contentAgree': '5',
            'answerOrderBy': 'agree',
            'questionOrderBy': 'agreeCount',
        }
        self.initconfig()
        self.config.read('setting.ini')  # ????
        self.getSetting(self.settingList)

    def initconfig(self):
        u"""
        初始化配置文件的配置信息
        :return:
        """
        config = self.config
        if not os.path.isfile('setting.ini'):
            f = open('setting.ini', 'w')
            f.close()
            config.add_section('Zhihu2ebook')
            for key in self.setDict:
                config.set('Zhihu2ebook', key, self.setDict[key])
                print key + ":" + self.setDict[key]
            config.write(open('setting.ini', 'w'))
        return

    def getSetting(self, setting=[]):
        u"""
        输入要查询的setting的列表，返回查询到的字典
        获得配置文件的配置信息
        :param setting:
        :return:
        """
        config = self.config
        data = {}
        if config.has_section('Zhihu2ebook'):
            for key in setting:
                if config.has_option('Zhihu2ebook', key):
                    data[key] = config.get('Zhihu2ebook', key, raw=True)
                else:
                    data[key] = ''
        return data

    def setSetting(self, setting={}):
        u"""
        存储设置的信息
        :param setting: 传入的账号，密码信息的字典
        :return:
        """
        config = self.config
        if not config.has_section('Zhihu2ebook'):
            config.add_section('Zhihu2ebook')
        for key in self.settingList:
            if key in setting:
                config.set('Zhihu2ebook', key, str(setting[key]))
        config.write(open('setting.ini', 'w'))
        return

    def login_guide_account_password(self):
        print u'请输入用户名（知乎注册邮箱），回车确认'
        print u'直接回车使用内置账号登陆'
        account = raw_input()
        if len(account) == 0:
            account = "mengqingxue2014@qq.com"
            password = "131724qingxue"
        else:
            while re.search(r'\w+@[\w\.]{3,}', account) is None:   # 匹配邮箱的正则表达式，可以更完善
                print u'抱歉，输入的账号不规范...\n请输入正确的知乎登录邮箱\n'
                print u'账号要求：1.必须是正确格式的邮箱\n2.邮箱用户名只能由数字、字母和下划线_构成\n3.@后面必须要有.而且长度至少为3位'
                print u'范例：mengqingxue2014@qq.com\n5719abc@sina.cn'
                print u'请重新输入账号，回车确认'
                account = raw_input()
            print u'OK,验证通过\n请输入密码，回车确认'
            password = raw_input()
            while len(password) < 6:
                print u'密码至少6位起~'
                print u'范例：helloworldvia27149,51zhihu'
                print u'请重新输入密码，回车确认'
                password = raw_input()
        return account, password

    def login_guide_max_thread(self):
        print u'开始设置最大同时打开的网页数量，数值越大下载网页的速度越快，丢失答案的概率也越高，推荐值为5~50之间，在这一范围内助手可以很好的解决遗漏答案的问题，默认值为20'
        print u'请输入最大同时打开的网页数(1~199)，回车确认'
        try:
            max_thread = int(raw_input())
        except ValueError as error:
            print error
            print u'嗯，数字转换错误。。。最大线程数重置为20，点击回车继续'
            max_thread = 20
            raw_input()
        if max_thread > 200 or max_thread < 1:
            if max_thread > 200:
                print u'最大线程数溢出'
            else:
                print u'最大线程数非法，该值不能小于零'
            print u'最大线程数重置为20'
            max_thread = 20
            print u'点击回车继续~'
            raw_input()
        return max_thread

    def login_guide_pic_quality(self):
        print u'请选择电子书内的图片质量'
        print u'输入0为无图模式，所生成的电子书最小'
        print u'输入1为标准模式，电子书内带图片，图片清晰度能满足绝大多数答案的需要，电子书内的答案小于1000条时推荐使用'
        print u'输入2为高清模式，电子书内带为知乎原图，清晰度最高，但电子书体积是标准模式的4倍，只有答案条目小于100条时才可以考虑使用'
        print u'请输入图片模式(0、1或2)，回车确认'
        try:
            pic_quality = int(raw_input())
        except ValueError as error:
            print error
            print u'嗯，数字转换错误。。。'
            print u'图片模式重置为标准模式，点击回车继续'
            pic_quality = 1
            raw_input()
        if pic_quality != 0 and pic_quality != 1 and pic_quality != 2:
            print u'输入数值非法'
            print u'图片模式重置为标准模式，点击回车继续'
            pic_quality = 1
            raw_input()
        return pic_quality

# 测试
if __name__ == '__main__':
    # setting = Setting()    #   注意不要用这个setting
    # gotsettinglist = {}
    # gotsettinglist = setting.getSetting(['account', 'maxThread'])
    # for key in gotsettinglist:
    #     print key + ":" + gotsettinglist[key]
    pass
