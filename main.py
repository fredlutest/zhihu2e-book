# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Main.py
# Description :    程序的主要内容就在该类中的Main方法
# Author      :    Frank
# Date        :    2014.03.04
# ######################################################

from init import *
from login import *

class Zhihu2ebook(object):
    def __init__(self):
        u"""
        ContentList.txt存放需要爬取的地址（可能是收藏夹地址，可能是某用户的地址）
        ContentList.txt使用$符号区隔开，同一行内的链接信息会放在一本电子书中
        """
        self.check_update()   # 检查是否需要更新，如果有更新，默认浏览器打开链接
        init = Init()
        self.conn = init.getConn()  #
        self.cursor = self.conn.cursor()
        self.epubContent = {}   #
        self.epubInfolist = []  #
        self.baseDir = os.path.realpath('.')  # 获得当前目录的绝对路径
        self.setting = Setting()  # 用来获得设置信息

        # 获得几个配置的信息
        setting_dict = self.setting.getSetting(['rememberAccount', 'maxThread', 'picQuality'])
        self.reAccount = setting_dict['rememberAccount']
        self.mThread = setting_dict['maxThread']
        self.pQuality = setting_dict['picQuality']
        return

    def main_start(self):
        u"""
        程序运行的主函数
        :return:
        """
        if self.mThread == '':    # 如果线程数没有设置
            self.mThread = 5    # 默认线程数是5
        else:
            self.mThread = int(self.mThread)

        if self.pQuality == '':    # 如果没有设置照片
            self.pQuality = 1    # 有图，非高清
        else:
            self.pQuality = int(self.pQuality)

        login = Login(self.conn)
        if self.reAccount != 'yes':
            print u'检测到有设置文件，是否直接使用之前的设置？(帐号、密码、图片质量、最大线程数)'
            print u'直接点按回车使用之前设置，敲入任意字符后点按回车进行重新设置'
            if raw_input() == '':
                print "TODO, 利用保存的设置登陆"
            else:
                login.login()    # 不用之前的设置，重新登陆
                self.mThread = int(self.setting.login_guide_max_thread())
                self.pQuality = int(self.setting.login_guide_pic_quality())
        else:
            login.login()
            self.mThread = int(self.setting.login_guide_max_thread())
            self.pQuality = int(self.setting.login_guide_pic_quality())

        self.setting = Setting()
        settingDict = {
            'maxThread': self.mThread,
            'picQuality': self.pQuality,
        }
        self.setting.setSetting(settingDict)
        print "登陆成功，信息已经保存"

        # 主程序开始运行
        readList = open('./ReadList.txt', 'r')
        bookCount = 1
        for line in readList:
            # 一行表示一本电子书
            chapter = 1
            for rawUrl in line.split('$'):
                print u'正在制作第{}本电子书的第{}节'.format(bookCount, chapter)

    def getUrlInfo(self, rawUrl):
        u"""
        返回标准格式的网址
        返回查询所需要的内容
        urlInfo 结构
        *   kind
            *   answer
                *   questionID
                *   answerID
            *   question
                *   questionID
            *   author
                *   authorID
            *   collection
                *   colliectionID
            *   table
                *   tableID
            *   topic
                *   topicID
            *   article
                *   columnID
                *   articleID
            *   column
                *   columnID
        *   guide
            *   用于输出引导语，告知用户当前工作的状态
        *   worker
            *   用于生成抓取对象，负责抓取网页内容
        *   filter
            *   用于生成过滤器，负责在数据库中提取答案，并将答案组织成便于生成电子书的结构
        *   urlInfo
            *   用于为Author/Topic/Table获取信息
        *   baseSetting
            *   基础的设置信息，比如图片质量，过滤标准
            *   picQuality
                *   图片质量
            *   maxThread
                *   最大线程数
        """
        urlInfo = {}
        urlInfo['baseSetting'] = {}
        urlInfo['baseSetting']['picQuality'] = self.pQuality
        urlInfo['baseSetting']['maxThread'] = self.mThread
        def detectUrl(rawUrl):
            targetPattern = {}
            targetPattern['answer'] = r'(?<=zhihu\.com/)question/\d{8}/answer/\d{8}'
            targetPattern['question'] = r'(?<=zhihu\.com/)question/\d{8}'
            # 使用#作为备注起始标识符，所以在正则中要去掉#
            targetPattern['author'] = r'(?<=zhihu\.com/)people/[^/#\n\r]*'
            targetPattern['collection'] = r'(?<=zhihu\.com/)collection/\d*'
            targetPattern['table'] = r'(?<=zhihu\.com/)roundtable/[^/#\n\r]*'
            targetPattern['topic'] = r'(?<=zhihu\.com/)topic/\d*'
            # 先检测专栏，再检测文章，文章比专栏网址更长，类似问题与答案的关系，取信息可以用split('/')的方式获取
            targetPattern['article'] = r'(?<=zhuanlan\.zhihu\.com/)[^/]*/\d{8}'
            targetPattern['column'] = r'(?<=zhuanlan\.zhihu\.com/)[^/#\n\r]*'
            # TODO


    def check_update(self):
        u"""
        TODO：
        利用网络上某个文件的内容（时间对比）检查是否需要更新，如果时间信息是新的，
        自动用默认浏览器打开连接，（打算将最新版本链接置为百度网盘链接）
        :return:
        """
        print u"检查是否有新版本..."
