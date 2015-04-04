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
                login.login()    #  不用之前的设置，重新登陆
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


    def check_update(self):
        u"""
        TODO：
        利用网络上某个文件的内容（时间对比）检查是否需要更新，如果时间信息是新的，
        自动用默认浏览器打开连接，（打算将最新版本链接置为百度网盘链接）
        :return:
        """
        print u"检查是否有新版本..."

    def getURLInfo(self, url):
        u"""
        TODO:
        通过模式匹配将要查询的网址，确定匹配类型
        返回标准格式的网址以及相关信息
        """
        urlInfo = {}

        urlInfo['baseSetting']['pQuality'] = self.pQuality
        urlInfo['baseSetting']['mThread'] = self.mThread

        def detectURL(url):

            urlPattern = {}
            urlPattern['answer']     = r'(?<=zhihu\.com/)question/\d{8}/answer/\d{8}'
            urlPattern['question']   = r'(?<=zhihu\.com/)question/\d{8}'
            urlPattern['author']     = r'(?<=zhihu\.com/)people/[^/#\n\r]*'#使用#作为备注起始标识符，所以在正则中要去掉#
            urlPattern['collection'] = r'(?<=zhihu\.com/)collection/\d*'
            urlPattern['table']      = r'(?<=zhihu\.com/)roundtable/[^/#\n\r]*'
            urlPattern['topic']      = r'(?<=zhihu\.com/)topic/\d*'
            urlPattern['article']    = r'(?<=zhuanlan\.zhihu\.com/)[^/]*/\d{8}'#先检测专栏，再检测文章，文章比专栏网址更长，类似问题与答案的关系，取信息可以用split('/')的方式获取
            urlPattern['column']     = r'(?<=zhuanlan\.zhihu\.com/)[^/#\n\r]*'

            #for key in urlPattern:  这样不行吗？
            for key in ['answer', 'question', 'author', 'collection', 'table', 'topic', 'article', 'column']:
                urlInfo['url'] = re.serach(urlPattern[key],url)
                if urlInfo['url'] != None:
                    urlInfo['type'] = key
                    if key != 'article' and key != 'column':
                        urlInfo['baseUrl']  = 'http://www.zhihu.com/' + urlInfo['url'].group(0)
                    else:
                        urlInfo['baseUrl']  = 'http://zhuanlan.zhihu.com/' + urlInfo['url'].group(0)
                    return key
        return ''

        type = detectURL(url)

        if type == 'answer':
            urlInfo['questionID'] = re.search(r'(?<=zhihu\.com/question/)\d{8}', urlInfo['baseUrl']).group(0)
            urlInfo['answerID'] = re.search(r'(?<=zhihu\.com/question/\d{8}/answer/)\d{8}', urlInfo['baseUrl']).group(0)
            urlInfo['guide'] = u'成功匹配到答案地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker'] = AnswerWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter'] = AnswerFilter(self.cursor, urlInfo)
            urlInfo['infoUrl'] = ''
        if type == 'question':
            urlInfo['questionID']   = re.search(r'(?<=zhihu\.com/question/)\d{8}', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到问题地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = QuestionWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = QuestionFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = ''
        if type == 'author':
            urlInfo['authorID']     = re.search(r'(?<=zhihu\.com/people/)[^/#]*', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到用户主页地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = AuthorWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = AuthorFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = urlInfo['baseUrl'] + '/about'
        if type == 'collection':
            urlInfo['collectionID'] = re.search(r'(?<=zhihu\.com/collection/)\d*', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到收藏夹地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = CollectionWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = CollectionFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = urlInfo['baseUrl']
        if type == 'topic':
            urlInfo['topicID']      = re.search(r'(?<=zhihu\.com/topic/)\d*', urlInfo['baseUrl']).group(0)
            urlInfo['guide']        = u'成功匹配到话题地址{}，开始执行抓取任务'.format(urlInfo['baseUrl'])
            urlInfo['worker']       = TopicWorker(conn = self.conn, urlInfo = urlInfo)
            urlInfo['filter']       = TopicFilter(self.cursor, urlInfo)
            urlInfo['infoUrl']      = urlInfo['baseUrl']
        if type == 'table':
            urlInfo['tableID']      = re.search(r'(?<=zhihu\.com/roundtable/)[^/#]*', urlInfo['baseUrl']).group(0)
        if type == 'article':
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)[^/]*', urlInfo['baseUrl']).group(0)
            urlInfo['articleID']    = re.search(r'(?<=zhuanlan\.zhihu\.com/' + urlInfo['columnID'] + '/)' + '\d{8}', urlInfo['baseUrl']).group(0)
        if type == 'column':
            urlInfo['columnID']     = re.search(r'(?<=zhuanlan\.zhihu\.com/)[^/]*', urlInfo['baseUrl']).group(0)
        return urlInfo