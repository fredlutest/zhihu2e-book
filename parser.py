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
        self.regDict['splitContent']    = r'<div tabindex="-1" class="zm-item-answer "'#关键表达式，用于切分答案
        self.regTipDict['splitContent'] = u'内容分割'

        # 提取答主的信息
        

    def add_regex(self):
        return