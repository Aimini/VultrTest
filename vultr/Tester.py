# -*- coding: utf-8 -*-
# time: 2018-11-06 19:46:13
# Author: AI
# Desc: test vultr speed
#  - main: test the best vultr server, include client-server ping\ server-client ping\ client download speed from server
#

import http.cookiejar
import io
import math
import os
import pathlib
import sys
import urllib
import winsound
from datetime import datetime
from urllib.request import OpenerDirector

import bs4
import chardet

# where can you get the server's list
from vultr import PingThread, publicIP
from vultr.Node import Node
from vultr.Result import Result
from vultr.ServerPing import vultr_server_ping, ServerPingThread
from vultr.SimulateData import vultrSimulateScore

vultrServerUrl = "https://www.vultr.com/faq/"
# servers Node list , name and Url
vultrServerNodes = []
# vultr test score
vultrServersScore = {}

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

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
    char_encode = chardet.detect(raw_text)
    print(char_encode)
    return raw_text.decode(encoding=char_encode['encoding'])


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


def put_ping_threads_result_to_map(result_map, ts):
    for t in ts:
        if (result_map[t.serverNode]) is None:
            result_map[t.serverNode] = Node()

        if type(t) is ServerPingThread:
            result_map[t.serverNode].sc = t.result
        if type(t) is PingThread:
            result_map[t.serverNode].cs = t.result


def multiple_thread_ping(server_nodes, result_map, thread_producer):
    client_ping_threads = [thread_producer(oneServerNode) for oneServerNode in server_nodes]
    for _ in client_ping_threads: _.start()
    for _ in client_ping_threads: _.join()
    put_ping_threads_result_to_map(result_map, client_ping_threads)


def client_ping(server_nodes, count, result_map):
    multiple_thread_ping(server_nodes, result_map, lambda node: PingThread(node, count))


def server_ping(server_nodes, target, count, result_map):
    multiple_thread_ping(server_nodes, result_map, lambda node: ServerPingThread(node, target, count))


def download_speed(link: str):
    response = urllib.request.urlopen(link)

    total_len = 0
    total_seconds = 0
    speed_avg = 0
    speed_max = 0
    block_len = 0

    block_start_time = datetime.today()
    start_time = datetime.today()
    while True:
        current = datetime.today()
        duration = (current - block_start_time).total_seconds()
        if duration > 1:
            speed = (block_len / (1024 ** 2)) / duration
            speed_max = max(speed_max, speed)
            # print(speed)
            block_start_time = current
            block_len = 0
        block = response.read(10240)
        block_len += len(block)
        total_len += len(block)
        if not block:
            break

    total_seconds = (datetime.today() - start_time).total_seconds()
    speed_avg = (total_len / (1024 * 1024)) / total_seconds
    print(total_len)
    return speed_avg, speed_max, total_seconds


def servers_download(server_nodes, result_map, useGB=True):
    for server in server_nodes:
        if useGB:
            url = server.get1GDownloadLink()
        else:
            url = server.get100MBDownloadLink()
        savg, smax, seconds = download_speed(url)
        print("{}:MB/s".format(server.name,savg))
        result_map[server].speed = [round(smax, 2), round(savg, 2)]


def print_as_table(result):
    # city name ,and result field column
    col_max_len = [0 for i in range(1 + len(list(result.values())[0].as_list()))]
    # calculate str max len in each column
    for k, v in result.items():
        # city name column
        col_max_len[0] = max(col_max_len[0], len(k.name))
        # result's member's columns
        for i in range(len(v.as_list())):
            col_max_len[i + 1] = max(col_max_len[i + 1], len(str(v.as_list()[i])), 4)

    format_str = ""
    i = 0
    for one_col in col_max_len:
        if i == 8 or i == 15:
            format_str += "| "
        format_str += "{{:<{}}}".format(one_col + 2)
        i += 1

    print(format_str.format("name",
                            "sent", "rec", "loss", "loss%",
                            "min", "max", "avg",
                            "sent", "rec", "loss", "loss%",
                            "min", "max", "avg", "max", "MB/s"))

    for k, v in result.items():
        print(format_str.format(k.name, *[round(i, 2) for i in (v.as_list())]))


def write_to_csv(result_map):
    filename = "vultr.csv"
    is_new = not os.path.exists(filename)
    file = open(filename, 'a')
    if is_new:
        file.write(",client,,,,,,,server,,,,,,,,,,\n"
                   ",package,,,,delay,,,package,,,,delay,,,speed,,,\n"
                   "name,sent,received,loss,loss rate,min,max,avg,sent,received,loss,loss rate,min,max,avg,max,avg,,\n")
    for k, v in result_map.items():
        file.write('"{}",'.format(k.name) + ",".join([str(i) for i in v.as_list()]) + ",,\n")
    file.close()


def main():
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
                # the second <td> is server node's url
                address = tds[1].a['href']
                vultrServerNodes.append(Node(name, address))
                vultrServersScore[vultrServerNodes[-1]] = Result()
        except TypeError as e:
            print("catch a TypeError,maybe server {0} will coming soon.")
            print(e)
            pass

    ping_count = 64
    client_ping(vultrServerNodes, ping_count, vultrServersScore)
    server_ping(vultrServerNodes, publicIP(), ping_count, vultrServersScore)
    servers_download(vultrServerNodes, vultrServersScore)
    print_as_table(vultrServersScore)
    write_to_csv(vultrServersScore)
    winsound.MessageBeep(winsound.MB_OK)


if __name__ == '__main__':
    main()
