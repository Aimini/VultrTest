from urllib.parse import urljoin


class Node:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def get1GdownloadLink(self):
        return urljoin(self.address, "vultr.com.1000MB.bin")

    def get100MBdownloadLink(self):
        return urljoin(self.address, "vultr.com.100MB.bin")

    def __str__(self):
        l = []
        for k, v in vars(self).items():
            if isinstance(v,str):
                l.append("{}='{}'".format(k, v))
            else:
                l.append("{}={}".format(k, v))
        return "{}({})".format(self.__class__.__name__,",".join(l))

    def __repr__(self):
        return str(self)