# -*- coding: utf-8 -*-
# time: 2018-11-06 19:46:13
# Author: AI

import re
import subprocess as sbp
import sys
import urllib.request
import ipaddress as ipadd
from urllib.parse import urlparse

from urllib.request import Request

import chardet


def ping(host: str, count: int = 4):
    """
    sending a ICMP Echo Request to the host with "count" times
    (detail with:https://searchnetworking.techtarget.com/definition/ping)
    :param host: target host, IP or URL
    :param count: times you want to diagnose
    :return a dict with key tow key {"package","delay"} that inclucde package info and delay info
        { "package": list() , "delay": list()}
        and The meaning of the package info list's elements is as follows:
        [sent, received, lost, lost_rate]
        and delay list:
        [minimum, maximum, average]
    """
    netloc = net_location(host)
    if sys.platform == 'win32':
        p_cmd = sbp.Popen(["cmd.exe", "/k", "chcp", "65001"], stderr=sbp.STDOUT, stdin=sbp.PIPE, stdout=sbp.PIPE,
                          shell=False, bufsize=1,
                          universal_newlines=True)
        out, err = p_cmd.communicate("ping {} -n {}\n".format(netloc, count))
        p_cmd.terminate()

        # "ping.exe",one_node.url,"-n",str(count)
        PLP = re.search(r"Packets: Sent = (\S+), Received = (\S+), Lost = (\S+) \((\S+)% loss\)", out)
        DELAY = re.search(r"Minimum = (\S+)ms, Maximum = (\S+)ms, Average = (\S+)ms", out)
        # if PLP and DELAY:
        node_data = {
            "package": [PLP.group(1), PLP.group(2), PLP.group(3), PLP.group(4)],
            "delay": [DELAY.group(1), DELAY.group(2), DELAY.group(3)]}

        return node_data


def publicIP():
    response = urllib.request.urlopen("http://2018.ip138.com/ic.asp")
    data = response.read()
    text = data.decode(chardet.detect(data)['encoding'])
    ip_str = re.search(r"您的IP是：\[(\S+)\] 来自：", text).group(1)
    return ipadd.IPv4Address(ip_str)


def net_location(url):
    # if host string is ip or none-protcol url,
    #  add the temp protcol, then use urlparse to get the net location
    parsed_url = urlparse(url)
    if parsed_url.scheme == "":
        host = "https://" + url
    return parsed_url.netloc
