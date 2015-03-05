import re
import HTMLParser


class Parse(object):
    """
    基类
    解析HTML字符串
    """
    def __init__(self, content):
        self.content = content.replace('\r', '').replace('\n', '')
        self.reg_dict = {}   # 这两行不应该放在init_regex函数中
        self.reg_tip_dict = {}

        self.init_regex()
        self.add_regex()

    def init_regex(self):
        # 关键表达式，用于切分答案
        self.reg_dict['splitContent'] = r'<div tabindex="-1" class="zm-item-answer "'
        self.regTipDict['splitContent'] = u'内容分割'

        # 提取答主的信息
        self.reg_dict['answerAuthorInfo'] = r'(?<=<h3 class="zm-item-answer-author-wrap">).*?(?=</h3>)'
        # 若为匿名用户，则收集到的内容只有【匿名用户】四个字
        self.reg_tip_dict['answerAuthorInfo'] = u'提取答主信息块'
        self.reg_dict['answerAuthorID']      = r'(?<=href="/people/)[^"]*'
        self.reg_tip_dict['answerAuthorID']   = u'提取答主ID'
        self.reg_dict['answerAuthorLogo']    = r'(?<=<img src=")[^"]*'
        self.reg_tip_dict['answerAuthorLogo'] = u'提取答主头像'
        self.reg_dict['answerAuthorSign']    = r'(?<=<strong title=").*(?=" class="zu-question-my-bio">)'
        # 可能没有
        self.reg_tip_dict['answerAuthorSign'] = u'提取答主签名'
        # 需要在用户名基础上进行二次匹配,正则模板直接放在了函数里
        self.reg_tip_dict['answerAuthorName'] = u'提取答主用户名'


    def add_regex(self):
        return
