# -*- coding: utf-8 -*-
# time: 2018-11-06 19:46:13
# Author: AI
# Desc: test vultr speed
#  - main: test the best vultr server, include client-server ping\ server-client ping\ client download speed from server
#

import io
import sys
import chardet

import urllib
import http.cookiejar
from urllib.request import OpenerDirector

import bs4

# where can you get the server's list
vultrServerUrl = "https://www.vultr.com/faq/"
# servers Node list , name and Url
vultrServerNodes = []
# vultr test score
vultrserversScore = {}


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


default_headers = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36',
    'Referer': 'http://www.baidu.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}


def make_opener(head=None) -> OpenerDirector:
    if head is None:
        head = default_headers
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []  # 字典转换成元组集合
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


def as_text(data):
    raw_text = data.read()
    charencode = chardet.detect(raw_text)
    print(charencode)
    return raw_text.decode(encoding=charencode['encoding'])


opener = make_opener()
html_text = as_text(opener.open("https://www.vultr.com/faq/"))


# TODO: get server's link