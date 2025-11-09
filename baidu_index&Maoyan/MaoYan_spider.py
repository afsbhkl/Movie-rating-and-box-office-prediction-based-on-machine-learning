import requests
import time
import random
import hashlib
import csv
import os
import re
import pandas as pd
from lxml import etree
from io import BytesIO
from loguru import logger
from fake_useragent import UserAgent
from fontTools.ttLib import TTFont

df = pd.read_excel('./movie.xlsx')
cookies = {
    '_lxsdk_cuid': '184db05792ec8-060eaf94dc7e51-26021f51-144000-184db05792ec8',
    '__mta': '107442621.1670121880170.1676707250020.1676708236118.8',
    'uuid_n_v': 'v1',
    'uuid': 'C5765360924C11EEBF0AAFDCFAC3033FBB5F06E8AA0A4B2A9C88D4E763F66D9D',
    '_lxsdk': 'C5765360924C11EEBF0AAFDCFAC3033FBB5F06E8AA0A4B2A9C88D4E763F66D9D',
    '_csrf': '81fcaba32e1e7e2dbeaddf4276678dae667fa08e4688496a885b3fa4042e577e',
    'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2': '1701656892,1702564068,1702645612,1702699413',
    '_lxsdk_s': '18c70cb2ee3-f8d-773-b56%7C%7C2',
    'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2': '1702699443',
}


class MaoYan:
    def __init__(self):
        if not os.path.exists('./MaoYan.txt'):
            self.MaoYan = list()
        else:
            self.MaoYan = [i.strip() for i in open('MaoYan.txt', 'r', encoding='utf8').readlines()]
        self.file = open("猫眼.csv", "a", encoding="utf-8", newline="")
        self.csv_writer = csv.DictWriter(self.file, ['title', '评分', '家长引导', '出品发行', '技术参数', '获奖', '提名', '最佳影片'])
        self.csv_writer.writeheader()
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': UserAgent().chrome,
            'Referer': 'https://www.maoyan.com/films/1211270',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            #'Cookie': '_lxsdk_cuid=184db05792ec8-060eaf94dc7e51-26021f51-144000-184db05792ec8; __mta=107442621.1670121880170.1676707250020.1676708236118.8; uuid_n_v=v1; uuid=C5765360924C11EEBF0AAFDCFAC3033FBB5F06E8AA0A4B2A9C88D4E763F66D9D; _lxsdk=C5765360924C11EEBF0AAFDCFAC3033FBB5F06E8AA0A4B2A9C88D4E763F66D9D; _csrf=9c04575b74b473b8d680d1148f40f875a4c4c538da14da69397288a249e31c0f; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1701656892,1702564068,1702645612; _lxsdk_s=18c6d963d67-289-22b-c3a%7C%7C14; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1702650764'
        }

    def get_data(self, url, md5):
        params = {
            'timeStamp': time.time()*1000,
            'index': int(random.random()*10)+1,
            'signKey': md5,
            'channelId': '40011',
            'sVersion': '1',
            'webdriver': 'false'
        }
        try:
            response = requests.get(url=url, headers=self.headers, params=params, cookies=cookies)
            return response
        except Exception as e:
            print("重试中...", e)
            time.sleep(random.randint(10, 30))
            self.get_data(url, md5)

    def get_md5(self):
        f = f'method=GET&timeStamp={time.time()*1000}&User-Agent={UserAgent().chrome}&index={int(random.random()*10)+1}&channelId=40011&sVersion=1&key=A013F70DB97834C0A5492378BD76C53A'
        md5 = hashlib.md5()
        md5.update(f.encode('utf-8'))
        sign = md5.hexdigest()
        return sign

    def main(self):
        # 'https://www.maoyan.com/ajax/films/1211270'
        urls = [i for i in df['href']]
        count = 0
        for url in urls:
            print('--------------------正在解析第{}条数据--------------------'.format(count+1))
            self.headers['Referer'] = url
            new_url_ = 'https://www.maoyan.com/ajax/films/' + str(url).split('/')[-1]
            if new_url_ in self.MaoYan:
                count += 1
                print('数据已存在...')
                continue
            print(df['title'][count])
            md5 = self.get_md5()
            resp = self.get_data(new_url_, md5)
            # 下载字体文件
            font_url = 'https:' + ''.join(re.findall(r'format\("embedded-opentype"\),url\("(.*)"\)', resp.text))  # 替换为实际的字体文件URL
            res = requests.get(font_url, headers=self.headers)
            font = TTFont(BytesIO(res.content))
            keys = font.getGlyphNames()[1:-1]
            xxx = []
            for key in keys:
                x_y = list(font['glyf'][key].coordinates)
                xxx.append((key, x_y[-1][0] - x_y[0][0]))
            xxx.sort(key=lambda x: x[1])
            yyy = [2, 6, 4, 5, 3, 8, 1, 0, 9, 7]
            zzz = dict()
            for m, n in enumerate(xxx):
                name = '&#x'+n[0][3:].lower()+';'
                zzz[name] = yyy[m]
            # print(zzz)
            page_data = resp.text
            for m, n in zzz.items():
                page_data = page_data.replace(m, str(n))
            # print(page_data)
            html = etree.HTML(page_data)
            dit = {
                'title': df['title'][count],
                '评分': ''.join(html.xpath('//div[@class="movie-stats-container"]/div[1]/div/div/span/span/text()')).encode('utf-8').decode('utf-8'),
                '家长引导': ''.join(html.xpath('//div[@class="tab-content-container"]/div[1]/div[6]/div[2]/div/div[1]/div[2]/text()')),
                '出品发行': ''.join(html.xpath('//div[@class="tab-content-container"]/div[1]/div[6]/div[2]/div/div[2]/div[2]/text()')),
                '技术参数': ''.join(html.xpath('//div[@class="tab-content-container"]/div[1]/div[6]/div[2]/div/div[3]/div[2]/text()')),
                '获奖': ''.join(html.xpath('//div[@class="tab-content-container"]/div[1]/div[7]/div[2]/div/div[1]/div[1]/text()')),
                '提名': ''.join(html.xpath('//div[@class="tab-content-container"]/div[1]/div[7]/div[2]/div/div[2]/div[1]/text()')),
                '最佳影片': ''.join(html.xpath('//div[@class="tab-content-container"]/div[1]/div[7]/div[2]/div/div[3]/div[1]/text()'))
            }
            logger.info(dit)
            self.csv_writer.writerow(dit)
            with open('MaoYan.txt', 'a', encoding='utf-8') as w:
                w.write('{}\n'.format(new_url_))
            time.sleep(random.randint(3, 10))

            count += 1
        self.file.close()


if __name__ == '__main__':
    m = MaoYan()
    m.main()
