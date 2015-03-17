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
import os

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
        # ConfigParser这个类能够很好地操作ini格式的文件（配置文件）
        # 看完删掉上一行  --何俊 03.06
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

# 测试
if __name__ == '__main__':
    setting = Setting()
    gotsettinglist = {}
    gotsettinglist = setting.getSetting(['account', 'maxThread'])
    for key in gotsettinglist:
        print key + ":" + gotsettinglist[key]

