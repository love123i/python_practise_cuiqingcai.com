#!/usr/bin/env python
# encoding:utf-8
# 04_mm_at_taobao.py
# 2016/7/12  13:40

'''
抓取淘宝MM照片
教程链接：http://cuiqingcai.com/1001.html
'''
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import os, re, json
import codecs

class MM_Taobao(object):

    def __init__(self):
        self.url_protocol = 'https:'
        self.url_base = 'https://mm.taobao.com/json/request_top_list.htm?page=%d'
        self.url_albums = 'https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id=%s'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'mm.taobao.com'
        }
        self.path_current = os.path.join(os.path.dirname(os.path.abspath('.')), 'mm_images')

    def _get(self, url, params=None, **kwargs):
        return requests.get(url, params, headers=self.headers, **kwargs)

    def _post(self, url, data=None, **kwargs):
        return requests.post(url, data=data, **kwargs)

    def _get_soup(self, html):
        return BeautifulSoup(html,'html5lib')



    def save_img(self, url_image, dirname, filename):
        '''
        从指定URL保存图片到磁盘（Image）
        '''
        path = os.path.join(self.path_current, dirname)
        self.mkdir(path)
        path = os.path.join(path, filename)

        # resp = self._get(url_image)
        resp = requests.get(url_image, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'gtd.alicdn.com'
        })
        img = resp.content

        with open(path, mode='wb') as fp:
            fp.write(img)

    def save_brief(self, content, name):
        '''
        将指定文本内容保存到磁盘（txt）
        '''
        path = os.path.join(self.path_current, name)
        filename = os.path.join(path, name+'.txt')
        self.mkdir(path)

        with codecs.open(filename,mode='w+',encoding='utf-8') as fp:
            fp.write(content)


    def mkdir(self, path):
        '''
        创建文件夹
        '''
        is_exist = os.path.exists(path)
        if is_exist:
            return False

        os.makedirs(path)
        return True

    def get_page(self, page=1):
        '''
        获取单页面内容，解析：
            1、MM链接
            2、MM头像
            3、MM名字
            4、MM年龄
            5、MM位置

        :return
            [{'name':name, 'id':id, 'age':age, 'location':location, 'url':url}]
        '''
        url = self.url_base % page
        resp = self._get(url)
        resp.encoding = 'gbk'

        re_user_id = re.compile(r'user_id=(\d{5,15})$')

        soup = self._get_soup(resp.text)
        item_list_soup = soup.find_all('div',{'class':'list-item'})
        item_list = []
        for item_soup in item_list_soup:
            _avatar_soup = item_soup.find('a',{'class':'lady-avatar'})
            mm_url_index = _avatar_soup['href']     # MM主页，但是需要登录淘宝账号才能访问
            mm_image = _avatar_soup.img['src']      # 头像，60x60

            _name_soup = item_soup.find('a',{'class':'lady-name'})
            mm_url_card = self.url_protocol + _name_soup['href']        # MM展示页面，通过该链接可查找到相册
            mm_name = _name_soup.getText()

            _top_soup = item_soup.find('p',{'class':'top'})
            mm_age = _top_soup.em.getText()
            mm_location = _top_soup.span.getText()

            mm_id = re_user_id.search(mm_url_card).group(1)
            item = {'name':mm_name, 'age':mm_age, 'location':mm_location, 'url':mm_url_card, 'id':mm_id}
            item_list.append(item)

        return item_list

    def start(self, page_start=1, page_end=1):
        '''
        总的大概在4300页左右
        '''
        start = page_start
        end = page_start if page_end < page_start else page_end
        while start<=end:
            print '开始抓取第 %s 页' % start
            page_result = self.get_page(1)
            for index,r in enumerate(page_result):
                print ' '*10 + '%s/%s抓取用户 %s@%s 的相册... ' % (index, len(page_result), r['name'], r['id'])
                mm.get_albums(user_id=r['id'])


    def get_album(self, url):
        '''
        传入单个相册的URL，获取该URL下所有的MM图片链接，返回 [mm_url*]
        '''
        re_user_id = re.compile(r'user_id=(\d*)')
        user_id = re_user_id.search(url).group(1)

        re_album_id = re.compile(r'album_id=(\d*)')
        album_id = re_album_id.search(url).group(1)

        url_template = r'https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id={user_id}&album_id={album_id}&page={page}'

        url = url_template.format(user_id=user_id, album_id=album_id, page=1)
        resp_json = self._get(url).json()

        url_transfer = self.url_protocol + resp_json['picList'][0]['url']
        resp_transfer = self._get(url_transfer)

        soup = self._get_soup(resp_transfer.text)
        pic_list_origin = json.loads(soup.find('input',{'id':'J_MmPicListId'})['value'])
        pic_list = []
        for pic in pic_list_origin:
            pic_list.append({'id':pic['picId'], 'url':self.url_protocol + pic['bigUrl']})

        return album_id, pic_list



    def get_albums(self, user_id):
        '''
        根据MM展示页url，采集其相册内所有图片
        '''
        url = self.url_albums % user_id
        resp = self._get(url)

        soup = self._get_soup(resp.text)
        photo_list_soup = soup.find_all('div',{'class':'mm-photo-cell'})

        # 获取该 user_id下所有的相册链接URL
        url_album_list = []
        for photo_soup in photo_list_soup:
            url_album = self.url_protocol + photo_soup.find('a', {'class': 'mm-first'})['href']
            url_album_list.append(url_album)

        # 根据上面获取到的所有相册链接URL，依次获取单个相册内的所有图片
        url_album = []
        for url_album in url_album_list:
            album_id, image_list = self.get_album(url_album)
            print ' ' * 23 + '抓取相册 %s' % album_id
            for image in image_list:
                # print image['url'], album_id, image['id']+'.jpg'
                self.save_img(image['url'], user_id + os.path.sep + album_id, image['id']+'.jpg')


if __name__ == '__main__':
    mm = MM_Taobao()
    mm.start(page_start=2)
    # mm.get_page(1)
    # mm.get_albums(user_id='687471686')
    # album_id, images = mm.get_album(url='https://mm.taobao.com/self/album_photo.htm?user_id=687471686&album_id=10000702574&album_flag=0')
    # mm.save_img('https://gtd.alicdn.com/imgextra/img.alicdn.com/imgextra/i2/687471686/TB15e8hMXXXXXc5aXXXXXXXXXXX_!!0-tstar.jpg_620x10000.jpg','10000702574','10002816410.jpg')
