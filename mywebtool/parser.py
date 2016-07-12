#!/usr/bin/env python
# encoding:utf-8
# parser.py
# 2016/7/7  9:48

def parse_cookies(_cookies):
    '''
    由于豆瓣的反爬虫机制，因此访问时加入cookie可以一定程度上避免403
    传入的 _cookies 由Chrome抓取，使用 parse_cookies 将其格式转换为dict

    >>> _cookies = 'bid=NmdRm269u2s; viewed="3288908"; gr_user_id=a89278d7-bf6f-47da-a708-5df179d23862; ll="118201"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1467787970%2C%22http%3A%2F%2Fxlzd.me%2F2015%2F12%2F16%2Fpython-crawler-03%22%5D; _pk_id.100001.4cf6=46892f084c622653.1467779927.3.1467791178.1467785992.; _pk_ses.100001.4cf6=*; __utma=30149280.96114181.1467779634.1467785990.1467788260.3; __utmb=30149280.0.10.1467788260; __utmc=30149280; __utmz=30149280.1467779634.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.2131815763.1467779927.1467785990.1467788260.3; __utmb=223695111.0.10.1467788260; __utmc=223695111; __utmz=223695111.1467779927.1.1.utmcsr=xlzd.me|utmccn=(referral)|utmcmd=referral|utmcct=/2015/12/16/python-crawler-03'
    >>> print parse_cookies(_cookies)
    {'__utmz': '223695111.1467779927.1.1.utmcsr=xlzd.me|utmccn=(referral)|utmcmd=referral|utmcct=/2015/12/16/python-crawler-03', 'bid': 'NmdRm269u2s', 'gr_user_id': 'a89278d7-bf6f-47da-a708-5df179d23862', '_pk_ses.100001.4cf6': '*', '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1467787970%2C%22http%3A%2F%2Fxlzd.me%2F2015%2F12%2F16%2Fpython-crawler-03%22%5D', '_pk_id.100001.4cf6': '46892f084c622653.1467779927.3.1467791178.1467785992.', '__utma': '223695111.2131815763.1467779927.1467785990.1467788260.3', '__utmb': '223695111.0.10.1467788260', '__utmc': '223695111', 'll': '"118201"', 'viewed': '"3288908"'}
    '''
    cookies = {}
    for line in _cookies.split(';'):
        name, value = line.strip().split('=',1)
        cookies[name] = value
    return cookies

if __name__ == '__main__':
    import doctest
    doctest.testmod()