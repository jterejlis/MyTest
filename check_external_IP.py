from urllib.request import urlopen
import re as r


def check_external_IP():

    d = str(urlopen('http://checkip.dyndns.com/')
            .read())

    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

