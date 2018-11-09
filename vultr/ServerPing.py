import re
import sys
import threading
import urllib.request
import math
import chardet


class ServerPingThread(threading.Thread):
    def __init__(self, serverNode, target, count=4):
        threading.Thread.__init__(self)
        self.serverNode = serverNode
        self.target = target
        self.count = count
        self.result = {}

    def run(self):
        print("ping server {}:".format(self.serverNode))
        self.result = vultr_server_ping(self.serverNode.url, self.target, self.count)


def vultr_server_ping(server_url, target, count=4):
    """
    ping target host from vultr server,
    the times you what to ping can only be a multiple of 4 because of vultr server limit.
    and also, loss package will not be count in it ,
    so the total package that you send not define to you
    in one word, we will excute ping command  ceil(count/4) times
    :param server_url: vultr server host(url or ip)
    :param target: target host , typically is you computer's public network IP
    :param count: times you want to ping(Can only be a multiple of 4)
    :return a dict with key tow key {"package","delay"} that inclucde package info and delay info
        { "package": list() , "delay": list()}
        and The meaning of the package info list's elements is as follows:
        [sent, received, loss, loss_rate]
        and delay list:
        [minimum, maximum, average]
    """
    count = math.ceil(count / 4)
    sent = 0
    received = 0

    delay_max = 0
    delay_min = sys.maxsize
    delay_avg = 0
    for i in range(count):
        server_url = "{}/ajax.php?cmd=ping&host={}".format(server_url, target)
        try:
            response = urllib.request.urlopen(server_url)
        except Exception as e:
            print("error server url:" + server_url)
            raise e
        data = response.read()
        text = data.decode(chardet.detect(data)['encoding'])

        PLP = re.search(r"(\S+) packets transmitted, (\S+) received, (\S+)% packet loss, time (\S+)ms", text)
        DELAY = re.search(r"rtt min/avg/max/mdev = (\S+)/(\S+)/(\S+)/(\S+)", text)
        if PLP is None or DELAY is None:
            print(text)
            return {"package": [-1, -1, -1, -1],
                    "delay": [-1, -1, -1]}
        sent += int(PLP.group(1))
        received += int(PLP.group(2))

        delay_max = max(delay_max, float(DELAY.group(1)))
        delay_avg += float(DELAY.group(2))
        delay_min = min(delay_min, float(DELAY.group(3)))

    delay_avg /= count
    loss = sent - received
    loss_rate = int(100 * loss / sent)

    return {"package": [sent, received, loss, round(loss_rate, 2)],
            "delay": [delay_max, delay_min, round(delay_avg, 2)]}
