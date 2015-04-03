# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    Login.py
# Description :    用于登陆的类
# Author      :    Frank
# Date        :    2014.03.04
# ######################################################


import urllib
import json
import datetime

from setting import *
from baseclass import *

from httpLib import *

class Login(BaseClass, HttpBaseClass, SqlClass, CookieBaseClass):
    """
    用于登陆网站的类
    @type dictionary: header
    """
    def __init__(self, conn):
        self.setting = Setting()
        self.conn = conn
        self.cursor = conn.cursor()
        # LWPCookieJar方法：创建与libwww-perl Set-Cookie3文件兼容的FileCookieJar实例 TODO
        self.cookieJarInMemory = cookielib.LWPCookieJar()
        # 产生管理器对象
        # urllib2()函数不支持验证，cookie或者其他HTTP高级功能，要支持这些功能，必须使用
        # build_opener()函数创建自定义Opener对象
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJarInMemory))
        urllib2.install_opener(self.opener)

    def login(self):
        self.login_guide()
        account, password = self.setting.login_guide_account_password()
        captcha = ''
        while not self.send_message(account, password, captcha):
            print u'啊哦，登录失败了'
            print u'请问是否需要更换登陆账号？输入『yes』后按回车可以更换账号密码'
            print u'或者猛击回车进入获取验证码的流程'
            confirm = raw_input()
            if confirm == 'yes':
                account, password = self.setting.login_guide_account_password()
            captcha = self.get_captcha()
        return

    def login_guide(self):
        print u'当然，作者更推荐您使用内置的孟晴雪的账号密码进行登陆，这能更好的保护您的账号密码安全'
        print u'现在开始登陆流程，请根据提示输入您的账号密码'

    def send_message(self, account, password, captcha=''):
        xsrf = self.getXsrf(self.get_http_content('http://www.zhihu.com/login'))
        print "debug: 输入的验证码：", captcha
        print "debug: 输入的用户：", account
        print "debug: 用户密码：", password

        if xsrf == '':
            print u'知乎网页打开失败'
            print u'回车重新发送登陆请求'
            return False
        _xsrf = xsrf.split('=')[1]
        # add xsrf as cookie into cookieJar,
        xsrfCookie = self.make_cookie(name='_xsrf', value=_xsrf, domain='www.zhihu.com')
        self.cookieJarInMemory.set_cookie(xsrfCookie)
        if captcha == '':    # 如果没有验证码
            loginData = '{0}&email={1}&password={2}'.format(xsrf, account, password, ) + '&rememberme=y'
        else:
            print "captchar到底怎么错了？", captcha
            loginData = '{0}&email={1}&password={2}&captcha={3}'.format(xsrf, account, password, captcha) + '&rememberme=y'
        loginData = urllib.quote(loginData, safe='=&')     # 表示不要对=&编码
        # 这里的警告是Pycharm的bug
        # http://stackoverflow.com/questions/8406242/why-does-pycharms-inspector-complain-about-d
        header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',    # 主要属性，只要有此项知乎即认为来源非脚本（怎么知道的。。。）
            'Accept-Language': 'zh,zh-CN;q=0.8,en-GB;q=0.6,en;q=0.4',
            'Connection': 'keep-alive',
            'Host': 'www.zhihu.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',  # 下面那行可能出问题？！
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/34.0.1847.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        header['Origin'] = 'http://www.zhihu.com'
        header['Referer'] = 'http://www.zhihu.com/'

        # 登陆时需要手工写urlopen，否则无法获取返回的信息
        request = urllib2.Request(url='http://www.zhihu.com/login', data=loginData)

        for headerKey in header.keys():
            request.add_header(headerKey, header[headerKey])

        try:
            result = urllib2.urlopen(request)
            jsonData = zlib.decompress(result.read(), 16 + zlib.MAX_WBITS)
            result = json.loads(jsonData)
            print "输出result:", result
        except Exception as error:
            print "in login.py send_message"
            print error
            return False

        if result['r'] == 0:
            print u'登陆成功'
            print u'登陆的账号为：', account
            print u'需要记住账号密码吗？输入yes回车表示记住，输入其他字符回车表示跳过'
            if raw_input() == 'yes':
                mysetting = {
                    'account': account,
                    'password': password,
                    'rememberAccount': 'yes',
                }
                self.setting.setSetting(mysetting)
                print u'账号密码已经保存，可以通过修改setting.ini文件修改账号密码等操作'
            else:
                mysetting = {
                    'account': '',
                    'password': '',
                    'rememberAccount': '',
                }
                self.setting.setSetting(mysetting)
                print u'跳过了保存账号密码'

            cookieJar2String = self.save_cookie_jar()
            data = dict()   # 上面说的那个Pycharmbug，这样写不会有警告
            data['account'] = account
            data['password'] = password
            data['recordDate'] = datetime.date.today().isoformat()
            data['cookieStr'] = cookieJar2String
            self.save2DB(cursor=self.cursor, data=data, primaryKey='account', tableName='LoginRecord')
            self.conn.commit()
            return True
        else:
            print u'登陆失败'
            self.print_dict(result)
            return False


    def get_captcha(self):
        buf = urllib2.urlopen(u'http://www.zhihu.com/captcha.gif')     # 获得验证码的图片
        f = open(u'验证码.gif', 'wb')
        f.write(buf.read())
        f.close()
        print u'验证码在程序运行的文件夹中，请输入验证码'
        captcha_str = raw_input()
        return captcha_str


    def save_cookie_jar(self):
        file_name = u'./cookie_jar_temp_file.txt'
        f = open(file_name, 'w')
        f.close()    # 创建文件
        self.cookieJarInMemory.save(file_name)
        f = open(file_name, 'r')
        content = f.read()
        f.close()
        os.remove(file_name)
        return content

    def load_cookie_jar(self, content=''):
        file_name = u'./cookie_jar_temp_file.txt'
        f = open(file_name, 'w')
        f.write(content)
        f.close()
        self.cookieJarInMemory.load(file_name)
        os.remove(file_name)
        return

    def get_cookie_header(self):
        cookie_str = ''
        for cookie in self.cookieJarInMemory:
            cookie_str += cookie.name + '=' + cookie.value + ';'
        return {'Cookie': cookie_str}

    def getXsrf(self, content=''):
        u"""
        提取xsrf信息
        """
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
        if xsrf == None:
            return ''
        else:
            return '_xsrf=' + xsrf.group(0)
