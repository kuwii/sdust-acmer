import socket
import urllib.request
import urllib.error


def get_page(url):
    req = urllib.request.Request(
        url,
        headers={
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
    )

    timeout = 30
    socket.setdefaulttimeout(timeout)

    try:
        op = urllib.request.urlopen(req, timeout=100)
        data = op.read()
        return data.decode('utf-8', 'ignore')
    except:
        return False
