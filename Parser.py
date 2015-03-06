# -*- coding:utf-8 -*-


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
        self.reg_tip_dict['splitContent'] = u'内容分割'

        # *********提取答主的信息*******************************************************************
        self.reg_dict['answerAuthorInfo'] = r'(?<=<h3 class="zm-item-answer-author-wrap">).*?(?=</h3>)'
        # 若为匿名用户，则收集到的内容只有【匿名用户】四个字
        self.reg_tip_dict['answerAuthorInfo'] = u'提取答主信息块'
        self.reg_dict['answerAuthorID'] = r'(?<=href="/people/)[^"]*'
        self.reg_tip_dict['answerAuthorID'] = u'提取答主ID'
        self.reg_dict['answerAuthorLogo'] = r'(?<=<img src=")[^"]*'
        self.reg_tip_dict['answerAuthorLogo'] = u'提取答主头像'
        self.reg_dict['answerAuthorSign'] = r'(?<=<strong title=").*(?=" class="zu-question-my-bio">)'
        # 可能没有
        self.reg_tip_dict['answerAuthorSign'] = u'提取答主签名'
        # 需要在用户名基础上进行二次匹配,正则模板直接放在了函数里
        self.reg_tip_dict['answerAuthorName'] = u'提取答主用户名'
        # *********提取答主的信息*******************************************************************

        # *********提取答案的信息*******************************************************************
        # 可能存在问题，当前测试样本中没有赞同数为0的情况，回去检查下
        self.reg_dict['answerAgreeCount'] = r'(?<=<div class="zm-item-vote-info " data-votecount=")[^"]*'
        self.reg_tip_dict['answerAgreeCount'] = u'提取答案被赞同数'
        # 为None
        self.reg_dict['answerCommentCount'] = r'\d*(?= 条评论)'
        self.reg_tip_dict['answerCommentCount'] = u'提取答案被评论数'
        self.reg_dict['answerCollectCount'] = r''
        # 只有在指定答案时才能用到
        self.reg_tip_dict['answerCollectCount'] = u'提取答案被收藏数'

        self.reg_dict['answerContent'] = r'(?<=<div class=" zm-editable-content \
        clearfix">).*?(?=</div></div><a class="zg-anchor-hidden ac")'
        self.reg_tip_dict['answerContent'] = r'提取答案内容'

        self.reg_dict['answerInfo'] = r'(?<=class="zm-meta-panel").*?(?=<a href="#" name="report" \
        class="meta-item zu-autohide">)'
        self.reg_tip_dict['answerInfo'] = r'提取答案信息'
        self.reg_dict['noRecordFlag'] = r'<span class="copyright zu-autohide"><span class="zg-bull">'
        self.reg_tip_dict['noRecordFlag'] = r'检查是否禁止转载'
        self.reg_dict['questionID'] = r'(?<= target="_blank" href="/question/)\d*'
        self.reg_tip_dict['questionID'] = u'提取问题ID'
        self.reg_dict['answerID'] = r'(?<= target="_blank" href="/question/\d{8}/answer/)\d*'
        self.reg_tip_dict['answerID'] = u'提取答案ID'
        # 没有考虑到只显示时间和昨天今天的问题
        self.reg_dict['updateDate'] = r'(?<=>编辑于 )[-:\d]*'
        self.reg_tip_dict['updateDate'] = u'提取最后更新日期'
        # 没有考虑到只显示时间和昨天今天的问题
        self.reg_dict['commitDate'] = r'(?<=发布于 )[-:\d]*'
        self.reg_tip_dict['commitDate'] = u'提取回答发布日期'
        # *********提取答案的信息*******************************************************************
        
        # 以下正则交由子类自定义之 
        # *********用戶首页信息提取*******************************************************************
        self.reg_dict['id'] = r''
        self.reg_dict['name'] = r''
        self.reg_dict['sign'] = r''
        self.reg_tip_dict['id'] = u'提取用户ID'
        self.reg_tip_dict['name'] = u'提取用户名'
        self.reg_tip_dict['sign'] = u'提取用户签名'
        
        self.reg_dict['followerCount'] = r''
        self.reg_dict['followCount'] = r''
        self.reg_tip_dict['followerCount'] = u'提取被关注数'
        self.reg_tip_dict['followCount'] = u'提取关注数'
        
        self.reg_dict['answerCount'] = r''
        self.reg_dict['questionCount'] = r''
        self.reg_dict['columnCount'] = r''
        self.reg_dict['editCount'] = r''
        self.reg_dict['collectionCount'] = r''
        self.reg_tip_dict['answerCount'] = u'提取回答总数'
        self.reg_tip_dict['questionCount'] = u'提取提问总数'
        self.reg_tip_dict['columnCount'] = u'提取专栏文章数'
        self.reg_tip_dict['editCount'] = u'提取公共编辑次数'
        self.reg_tip_dict['collectionCount'] = u'提取所创建的收藏夹数'
        
        self.reg_dict['agreeCount'] = r''
        self.reg_dict['thanksCount'] = r''
        self.reg_dict['collectedCount'] = r''
        self.reg_tip_dict['agreeCount'] = u'提取总赞同数'
        self.reg_tip_dict['thanksCount'] = u'提取总感谢数'
        self.reg_tip_dict['collectedCount'] = u'提取总收藏数'
        
        # 其它信息
        self.reg_dict['collectionID'] = r''
        self.reg_dict['collectionDesc'] = r''
        self.reg_dict['collectionFollower'] = r''
        self.reg_dict['collectionTitle'] = r''
        self.reg_dict['collectionComment'] = r''
        self.reg_dict['collectionCreaterID'] = r''
        self.reg_dict['collectionCreaterName'] = r''
        self.reg_dict['collectionCreaterSign'] = r''
        self.reg_tip_dict['collectionID'] = u'提取收藏夹ID'
        self.reg_tip_dict['collectionDesc'] = u'提取收藏夹描述'
        self.reg_tip_dict['collectionFollower'] = u'提取收藏夹被关注数'
        self.reg_tip_dict['collectionTitle'] = u'提取收藏夹标题'
        self.reg_tip_dict['collectionComment'] = u'提取收藏夹被评论数'
        self.reg_tip_dict['collectionCreaterID'] = u'提取收藏夹创建者ID'
        self.reg_tip_dict['collectionCreaterName'] = u'提取收藏夹创建者用户名'
        self.reg_tip_dict['collectionCreaterSign'] = u'提取收藏夹创建者签名'

        self.reg_dict['topicID'] = r''
        self.reg_dict['topicTitle'] = r''
        self.reg_dict['topicDesc'] = r''
        self.reg_dict['topicFollower'] = r''
        self.reg_tip_dict['topicID'] = u'提取话题ID'
        self.reg_tip_dict['topicTitle'] = u'提取话题名'
        self.reg_tip_dict['topicDesc'] = u'提取话题描述'
        self.reg_tip_dict['topicFollower'] = u'提取话题关注者人数'

        self.reg_dict['roundTableID'] = r''
        self.reg_dict['roundTableTitle'] = r''
        self.reg_dict['roundTableDesc'] = r''
        self.reg_dict['roundTableFollower'] = r''
        self.reg_tip_dict['roundTableID'] = u'提取圆桌ID'
        self.reg_tip_dict['roundTableTitle'] = u'提取圆桌标题'
        self.reg_tip_dict['roundTableDesc'] = u'提取圆桌描述'
        self.reg_tip_dict['roundTableFollower'] = u'提取圆桌关注者人数'
        # *********用戶首页信息提取*******************************************************************
        return

    def add_regex(self):
        return
