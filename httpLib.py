# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    httpLib.py
# Description :    http相关的方法，如decodeGZip，makeCookie等
# Author      :    Frank
# Date        :    2014.03.17
# ######################################################

import cookielib
import time
import zlib
import socket
import urllib2

def decodeGZip(rawPageData):
    """
    返回处理后的正常网页内容

    判断网页内容是否被压缩，无则直接返回，若被压缩则使用zlip解压后返回
    :param rawPageData: urlopen()传回的fileLike object
    :return: 页面内容，字符串或二进制数据|解压缩失败时则返回空字符串
    """

    if rawPageData.info().get(u"Content-Encoding") == "gzip":
        try:
            pageContent = zlib.decompress(rawPageData.read(), 16 + zlib.MAX_WBITS)
        except zlib.error as ziperror:
            print u'解压出错'
            print u'出错解压页面:' + rawPageData.geturl()
            print u'错误信息：'
            print zlib.error
            return ''
    else:
        pageContent = rawPageData.read()
        return pageContent

def getHttpContent(url='', extraHeader={}, data=None, timeout=5):
    """
    获取网页内容, 打开网页超过设定的超时时间则报错

    IOError:
    当解压缩页面失败时报错
    :param url: 待打开的网页
    :param extraHeader:  字典，添加需要的http头信息
    :param data:  需传输的数据，默认为空
    :param timeout: int格式的秒数，打开这个网页超过这个时间将直接退出，停止等待
    :return: 打开成功时返回页面内容，字符串或二进制数据，失败则返回空字符串
    """
    if data is None:
        request = urllib2.Request(url=url)
    else :
        request = urllib2.Request(url=url, data=data)
    for headerKey in extraHeader.keys():
        request.add_header(headerKey, extraHeader[headerKey])
    try:
        raw_page_data = urllib2.urlopen(request, timeout=timeout)
    except urllib2.HTTPError as error:
        print u'网页打开失败'
        print u'错误页面:' + url
        if hasattr(error, 'code'):
            print u'失败代码:' + str(error.code)
        if hasattr(error, 'reason'):
            print u'错误原因:' + error.reason
    except urllib2.URLError as error:
        print u'网络连接异常'
        print u'错误页面:' + url
        print u'错误原因:'
        print error.reason
    except socket.timeout as error:
        print u'打开网页超时'
        print u'超时页面' + url
    else:
        return decodeGZip(raw_page_data)
    return ''

def makeCookie(name, value, domain):
    cookie = cookielib.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=time.time() + 300000000,
        discard=False,
        comment=None,
        comment_url=None,
        rest={}
    )
    return cookie