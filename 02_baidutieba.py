#!/usr/bin/env python
# encoding:utf-8
# 02_baidutieba.py
# 2016/7/11  11:53
'''
百度贴吧内容抓取练习
'''
from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
from mywebtool.web_errors import HttpError
from mywebtool.tools import random_sleep
import codecs

class BDTB(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'tieba.baidu.com'
    }

    def __init__(self, baseUrl, seeLZ=False):
        self.url_base = baseUrl
        self.seeLZ = 1 if seeLZ==True else 0
        self.soup_default = self.get({'see_lz': self.seeLZ, 'pn': 1})
        self.page_num = self.get_page_num()
        self.title = '-'*15 + ' '*5 + self.get_title() + ' '*5 + '-'*15
        print self.title, 'total page: %d' % self.page_num

    def get(self, params=None):
        resp = requests.get(self.url_base, params=params)
        if resp.status_code != 200:
            raise HttpError(resp.status_code)

        '''
        'html.parser'           Python标准库
        'lxml'                  lxml HTML 解析器
        ['lxml','xml']、'xml'   lxml XML 解析器
        'html5lib'              html5lib
        '''
        soup = BeautifulSoup(resp.content, 'html5lib')
        try:
            status = soup.find('body')['class']
            if '404' in status[0]:
                raise HttpError(404)
        except KeyError:
            pass

        return soup

    def get_page(self, page_num):
        '''
        获取单页帖子内容
        return [{'author':author ,
                 'tail_floor':tail_floor,
                 'tail_time':tail_time,
                 'content':content} * ]
        '''
        if page_num == 1:
            soup = self.soup_default
        else:
            params = {'see_lz': self.seeLZ, 'pn': page_num}
            soup = self.get(params)

        title = soup.find('h3', attrs={'class':'core_title_txt pull-left text-overflow  ', 'title':True}).getText()
        item_list_soup = soup.find('div', attrs={'class':'p_postlist','id':'j_p_postlist'})
        item_list = []
        for index,item_soup in enumerate(item_list_soup):
            # 略过 script
            if item_soup.name != 'div':
                continue

            author = item_soup.find('li', attrs={'class':'d_name'}).a.getText()
            content = item_soup.find('div', attrs={'class':'d_post_content j_d_post_content '}).getText()
            tail_info = item_soup.find_all('span', attrs={'class':'tail-info'})
            tail_floor, tail_time = tail_info[-2].getText(), tail_info[-1].getText()
            item_list.append({'author':author, 'tail_floor':tail_floor, 'tail_time':tail_time, 'content':content})
            # item_list.append('{author}  {tail_floor}  时间:{tail_time}\n{content}\n'.format(author=author, tail_floor=tail_floor, tail_time=tail_time, content=content))

        #for item in item_list:
        #    print(item)
        return item_list

    def get_title(self):
        '''
        获取帖子的标题
        '''
        soup = self.soup_default
        title = soup.find('h3', attrs={'class': 'core_title_txt pull-left text-overflow  ', 'title': True}).getText()
        return title


    def get_page_num(self):
        '''
        获取该帖子的总页数
        '''
        soup = self.soup_default

        l_reply_num = soup.find('li',{'class':'l_reply_num'}).find_all('span')
        page_num = l_reply_num[1].getText()

        try:
            page_num = int(l_reply_num[-1].getText())
        except ValueError,e:
            page_num = 1
        return page_num

    def get_pages(self, file=None):
        '''
        获取帖子所有页的内容
            调用 self.get_page() 依次获取各页内容
        '''
        content_list = []
        for i in xrange(self.page_num):
            print 'getting page: %d' % i
            content = self.get_page(i)
            content_list.extend( content )
            random_sleep(0.5, log_pre='next page:%d total_page: %d' % (i,self.page_num))

        if file is not None:
            with codecs.open(file,mode='wb',encoding='utf-8') as fp:
                fp.write('{title}\n总页数:{page_num}页  URL:{url}\n\n'.format(title=self.title, page_num=self.page_num, url=self.url_base))
                for item in content_list:
                    fp.write('{author}  {tail_floor}  时间:{tail_time}\n{content}\n'.format(**item))

        return content_list


if __name__ == '__main__':
    import re
    id = raw_input('请输入帖子ID: ')
    re_url = re.compile(r'^\d{5,15}$')
    while not re_url.match(id):
        id = raw_input('请输入合法的帖子ID(纯数字): ')
    url = 'http://tieba.baidu.com/p/' + id
    seeLZ = input('是否只看楼主发言(0:否 1:是):')
    bdtb = BDTB(url, seeLZ=True if seeLZ==1 else False)
    bdtb.get_pages('baidutiezi.txt')