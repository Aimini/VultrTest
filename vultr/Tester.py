# -*- coding: utf-8 -*-
# time: 2018-11-06 19:46:13
# Author: AI
# Desc: test vultr speed
#  - main: test the best vultr server, include client-server ping\ server-client ping\ client download speed from server
#

import http.cookiejar
import io
import math
import pathlib
import sys
import urllib
import winsound
from urllib.request import OpenerDirector

import bs4
import chardet

# where can you get the server's list
from vultr import PingThread, publicIP
from vultr.Node import Node
from vultr.Result import Result
from vultr.ServerPing import vultr_server_ping, ServerPingThread

vultrServerUrl = "https://www.vultr.com/faq/"
# servers Node list , name and Url
vultrServerNodes = []
# vultr test score
vultrServersScore = {}

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


soup = getServerNodeListSoup(True)
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
            vultrServersScore[vultrServerNodes[-1]] = Result()
    except TypeError as e:
        print("catch a TypeError,maybe server {0} will coming soon.")
        print(e)
        pass

ping_count = 100
client_ping_threads = [PingThread(oneServerNode, ping_count) for oneServerNode in vultrServerNodes]
for _ in client_ping_threads: _.start()
for _ in client_ping_threads: _.join()
for t in client_ping_threads:
    pacakge = t.result['package']
    vultrServersScore[t.serverNode].setCSPackage(pacakge[0], pacakge[1], pacakge[2], pacakge[3])
    delay = t.result['delay']
    vultrServersScore[t.serverNode].setCSDelay(delay[0], delay[1], delay[2])

my_ip = publicIP()
server_ping_threads = [ServerPingThread(oneServerNode, my_ip, ping_count) for oneServerNode in vultrServerNodes]
for _ in server_ping_threads: _.start()
for _ in server_ping_threads: _.join()
for t in server_ping_threads:
    pacakge = t.result['package']
    vultrServersScore[t.serverNode].setSCPackage(pacakge[0], pacakge[1], pacakge[2], pacakge[3])
    delay = t.result['delay']
    vultrServersScore[t.serverNode].setSCDelay(delay[0], delay[1], delay[2])

# city name ,and result field column
col_max_len = [0 for i in range(15)]
# caculate str max len in each column  
for k, v in vultrServersScore.items():
    # city name column
    col_max_len[0] = max(col_max_len[0], len(k.name))
    # result's member's columns
    col_max_len[1] = 5
    col_max_len[2] = 5
    col_max_len[3] = 5
    col_max_len[4] = 6
    col_max_len[5] = max(col_max_len[5], len(str(v.CS_delay_min)))
    col_max_len[6] = max(col_max_len[6], len(str(v.CS_delay_max)))
    col_max_len[7] = max(col_max_len[7], len(str(v.CS_delay_avg)))
    col_max_len[8] = 5
    col_max_len[9] = 5
    col_max_len[10] = 5
    col_max_len[11] = 6
    col_max_len[12] = max(col_max_len[12], len(str(v.SC_delay_min)))
    col_max_len[13] = max(col_max_len[13], len(str(v.SC_delay_max)))
    col_max_len[14] = max(col_max_len[14], len(str(v.SC_delay_avg)))

format_str = ""
i = 0
for one_col in col_max_len:
    if i == math.ceil(len(col_max_len) / 2):
        format_str += "|"
    format_str += "%-{}s".format(one_col + 2)
    i += 1

print(format_str%("name",
                        "sent", "rec", "loss", "loss%",
                        "min", "max", "avg",
                        "sent", "rec", "loss", "loss%",
                        "min", "max", "avg"))

for k, v in vultrServersScore.items():
    print(format_str % (k.name,
          v.CS_sent, v.CS_received, v.CS_loss, v.CS_loss_rate,
          v.CS_delay_min, v.CS_delay_max, v.CS_delay_avg,
          v.SC_sent, v.SC_received, v.SC_loss, v.SC_loss_rate,
          v.SC_delay_min, v.SC_delay_max, v.SC_delay_avg))

winsound.MessageBeep(winsound.MB_OK)
