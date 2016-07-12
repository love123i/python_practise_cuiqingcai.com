#!/usr/bin/env python
# encoding:utf-8
# 01_qiushibaike.py
# 2016/7/11  10:31
'''
糗事百科  抓取热门段子
'''
from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import json


class QSBK(object):
    url_base = 'http://www.qiushibaike.com'
    url_hot = 'http://www.qiushibaike.com/hot/page/%s'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.qiushibaike.com'
    }

    def __init__(self):
        pass

    def get_hot(self, page=1):
        url = self.url_hot % page

        resp = requests.get(url, headers=self.headers)
        # print resp.content
        # print resp,resp.content
        '''
        'html.parser'           Python标准库
        'lxml'                  lxml HTML 解析器
        ['lxml','xml']、'xml'   lxml XML 解析器
        'html5lib'              html5lib
        '''
        soup = BeautifulSoup(resp.content, 'lxml')
        joke_list_soup = soup.find('div', attrs={'id':'content-left','class':'col1'})
        joke_list = []
        for joke_li in joke_list_soup.find_all('div',attrs={'class':'article block untagged mb15'}, recursive=False):
            author = joke_li.find('a',attrs={'title':True})['title']
            content = joke_li.find('div', attrs={'class':'content'}).getText()
            vote = joke_li.find('i', attrs={'class':'number'}).getText()
            img = joke_li.find('div', attrs={'class':'thumb'})
            if img is None:
                joke_list.append('Id:%s   author:{author}{content}Vote:{vote}\n{seperator}'.format(author=author, content=content, vote=vote,seperator='-'*50))
        # print json.dumps(joke_list, encoding='encoding-escape')
        for index, joke in enumerate(joke_list):
            print joke % index

if __name__ == '__main__':
    QSBK().get_hot()