# -*- coding: utf-8 -*-
# time: 2018-11-06 19:46:13
# Author: AI
# Desc: test vultr speed
#  - main: test the best vultr server, include client-server ping\ server-client ping\ client download speed from server
#

import http.cookiejar
import io
import os
import pathlib
import sys
import urllib
from urllib.request import OpenerDirector

import bs4
import chardet
import winsound

# where can you get the server's list
from vultr import ping, publicIP
from vultr.Node import Node

vultrServerUrl = "https://www.vultr.com/faq/"
# servers Node list , name and Url
vultrServerNodes = []
# vultr test score
vultrserversScore = {}

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

default_headers = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36',
    'Referer': 'https://www.vultr.com/',
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


def getServerNodeListSoup(useLocalCache=False):
    # BeautifulSoup can't process the file-like object,
    #  so you do not need to read string form file to buffer
    if useLocalCache:
        html_text = open(pathlib.Path(r"../cache/Vultr.com.html"))
    else:
        opener = make_opener()
        html_text = opener.open("https://www.vultr.com/faq/")
    soup = bs4.BeautifulSoup(html_text, 'lxml')
    return soup


soup = getServerNodeListSoup()
# each <tr> row meaing one server
tr_servers = soup.select("#speedtest_v4 tr")
# get the server node info form <tr>
for one_tr in tr_servers:
    tds = one_tr.find_all("td")
    try:
        name = tds[0].get_text().strip()
        address = ""
        if tds[1].a is not None:
            # the seconde <td> is server node's url
            address = tds[1].a['href']
            vultrServerNodes.append(Node(name, address))
    except TypeError as e:
        print("catch a TypeError,maybe server {0} will coming soon.")
        print(e)
        pass

#for oneServerNode in vultrServerNodes:
    #print(oneServerNode, end='')
    #print(ping(oneServerNode.url, 1))

my_ip = publicIP()
print(my_ip)
winsound.MessageBeep(winsound.MB_OK)