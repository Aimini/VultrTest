# -*- coding: utf-8 -*-
# time: 2018-11-06 19:46:13
# Author: AI
import socket
from urllib.parse import urljoin, urlparse

from vultr import net_location


class Node:
    def __init__(self, name, url, ip=None):
        self.name = name
        self.url = url
        if ip is None:
            self.ip = socket.gethostbyname(net_location(url))
        else:
            self.ip = ip

    def getNetLoc(self):
        return urlparse(self.url).netloc

    def get1GDownloadLink(self):
        return urljoin(self.url, "vultr.com.1000MB.bin")

    def get100MBDownloadLink(self):
        return urljoin(self.url, "vultr.com.100MB.bin")

    def __str__(self):
        l = []
        for k, v in vars(self).items():
            if isinstance(v, str):
                l.append("{}='{}'".format(k, v))
            else:
                l.append("{}={}".format(k, v))
        return "{}({})".format(self.__class__.__name__, ",".join(l))

    def __repr__(self):
        return str(self)
