import random
import time
import requests
import pandas as pd
import json
import csv
from fake_useragent import UserAgent
from loguru import logger
import os
import urllib3
urllib3.disable_warnings()  # 关闭证书警告


class BaiDuZs:
    def __init__(self):
        self.df = pd.read_excel('./movie.xlsx')
        self.cookies = {
              "MCITY": "-131%3A",
              "H_WISE_SIDS": "216849_213360_214793_110085_244716_259031_261716_236312_265883_266371_267371_265615_267072_268592_268706_268030_259642_269831_269904_269050_267066_256739_270335_270460_270548_271170_263618_271320_265032_270102_271812_269627_256151_234296_234207_272282_267596_272465_272830_260335_267558_273165_273120_273242_273300_273399_273389_271157_273479_273520_271147_273671_264170_270186_274078_273960_274141_274179_273918_273786_273044_273595_272858_256223_274412_272561_274440_274764_274760_270141_274777_274854_274856_274847_270158_275070_267806_267547_272333_275167_274335_275199_275149_274866_269286_274975_275778_270366_273491_275790_275825_275086_275994_275939_275970_274079_276089_269610_276061_276120_275915_275905_271119_276203_276250_274503_276196_276312_276160_276335_275170",
              "H_WISE_SIDS_BFESS": "216849_213360_214793_110085_244716_259031_261716_236312_265883_266371_267371_265615_267072_268592_268706_268030_259642_269831_269904_269050_267066_256739_270335_270460_270548_271170_263618_271320_265032_270102_271812_269627_256151_234296_234207_272282_267596_272465_272830_260335_267558_273165_273120_273242_273300_273399_273389_271157_273479_273520_271147_273671_264170_270186_274078_273960_274141_274179_273918_273786_273044_273595_272858_256223_274412_272561_274440_274764_274760_270141_274777_274854_274856_274847_270158_275070_267806_267547_272333_275167_274335_275199_275149_274866_269286_274975_275778_270366_273491_275790_275825_275086_275994_275939_275970_274079_276089_269610_276061_276120_275915_275905_271119_276203_276250_274503_276196_276312_276160_276335_275170",
              "PSTM": "1698991568",
              "BIDUPSID": "C99F83291D7930AF4644369D524D6903",
              "ZFY": "POwDHsvKc9Scm9FlviH1XokJY:An:AGILMskBRM:A8YBqc:C",
              "BAIDUID": "DDF519852F1F713A419924E37E5BB530:FG",
              "BAIDUID_BFESS": "DDF519852F1F713A419924E37E5BB530:FG",
              "H_PS_PSSID": "39712_39840_39904_39819_39909_39934_39937_39932_39940_39938_39931_39996",
              "Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc": "1702564074,1702620776,1702728872,1702790031",
              "BDUSS": "UxtSkc4ZEdwWVlOanhFLUJJclBpeVM1b3FUbU9LOH5vVThobHBTenZPVjJjYVpsRUFBQUFBJCQAAAAAAQAAAAEAAAAzp1B-SmVzc2ljYTAxMDkxNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHbkfmV25H5lV",
              "SIGNIN_UC": "70a2711cf1d3d9b1a82d2f87d633bd8a04528272888UiHt6lE5SG4q%2F2hMypCIxXLUKEIXapZCPvj90WPNw9Gjji3ika05ce0fboGmikkJF%2BVTKoNIRqkAM3bZ18lzU5ReT8HioMwgHMtrzkIbNWVIXRIjAubcKexWw6n%2BX0bNsUAIqED4B2F9epEabXrjEYcNttWHqz7wGiuGSPoXFKZP8JE3NYdXnpXUqWdTVO3gKOD32fRdy%2FFGRQUYNi7uZVBIJuIVC%2F%2BXuMOwzxx%2B3cj2CP6RHPpnAnRNskg2l5VScuoI5g0mR4t6MBKRkPAojWx0sWLusOwA6rJaZdHw%2BIY%3D91973152683930824246345949490459",
              "__cas__rn__": "452827288",
              "__cas__st__212": "f8bebd7eee04738dfed56fff12297d77bffb1d795c68f51e7b71b5d6af13e60aacd5de28f24d791357689100",
              "__cas__id__212": "52185775",
              "CPTK_212": "888882786",
              "CPID_212": "52185775",
              "bdindexid": "3hctbbu8onvrg0c58v0p5tjua3",
              "Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc": "1702814910",
              "RT": "\"z",
              "ab_sr": "1.0.1_MGVhMmQzZWJkZjk3OWEwOGE4MTM2MmU1NjZiODZhYjY2Mjk0NWQ1MzllMmI0ZWM1ODg3NDhlYzE5YmUyYTk1ZTJhNTRjOGJjYmJiOTBjNjYwNTRlYzc3Y2Y1Njk2MWIwZmQyODliZTc5NjNjZWRiYjUyZWUzOTMyY2NmMTM5ODdhYjc3MDFiMzUyMmFlZDRiODg1YTE2ZWJmMGZlMWQ0ZTc3NjkwMzRhZDk3NDY5NGVjODE1OGI1YjFlMDRhZTk1NDZiNmIxODVlNjQ5NzFkYjQzYzhmMzM0NWQ3YWJiMjM",
              "BDUSS_BFESS": "UxtSkc4ZEdwWVlOanhFLUJJclBpeVM1b3FUbU9LOH5vVThobHBTenZPVjJjYVpsRUFBQUFBJCQAAAAAAQAAAAEAAAAzp1B-SmVzc2ljYTAxMDkxNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHbkfmV25H5lV"
            }
        if not os.path.exists('./exist_news_url.txt'):
            self.exist_news_url = list()
        else:
            self.exist_news_url = [i.strip() for i in open('exist_news_url.txt', 'r', encoding='utf8').readlines()]
        self.file = open("百度指数.csv", "a", encoding="utf-8", newline="")
        self.csv_writer = csv.DictWriter(self.file, ['演员名称', '搜索指数整体日均值', '搜索指数移动日均值', '咨询指数日均值', ])
        self.csv_writer.writeheader()
        self.headers = {
            'User-Agent': UserAgent().chrome,
            'Host': 'index.baidu.com',
            'Referer': 'https://index.baidu.com/v2/main/index.html',
            'Cipher-Text': '1702738803496_1702813142472_xm6g4G4Gj0eW8vsoysSzhZlCTzRF29HCRjFVxMiomhDTsJZbPDldqE6MyJKVE1zlQODUHb+7TY9NBjPcINJsORQtiAdy3f8enSZ8wLZisMbeRYbqx6oEe5zA9PtTYRMc3miu8CVPtJiToe3kTCnbmaEBQ833+L3EAV8g4Rgv8+hV3mGZ0/fE83yR5BjIjkD6c6J7QkdWWr7ugtz9IvGL0+3a1FGd5M3vdmtKH0JfrLHyGfEFiQzjK1rdgglZ/t9o6GKbHKyF+eTQGqmg2GVbRDtYcrd1Ry4h5vxi3xsVTSzFa2U6tWytcpxJnFKWMk5gd8epnLwpvtrlNZQnfGAXSWdSADdrZEx6dHn+5IGmFauB5NhGTZWMJR9yWx3nz2k+',
        }

    def main(self):
        num = 0
        for i in self.df['actors']:
            if self.df['href'][num] in self.exist_news_url:
                num += 1
                print('数据已存在...')
                continue
            for actors_ in str(i).split('／'):
                session = requests.session()
                url = 'https://index.baidu.com/api/FeedSearchApi/getFeedIndex?word=[[%7B%22name%22:%22{}%22,%22wordType%22:1%7D]]&area=0&days=30'.format(actors_)  # 资讯指数url
                api_url = 'https://index.baidu.com/api/SearchApi/index?area=0&word=[[%7B%22name%22:%22{}%22,%22wordType%22:1%7D]]&startDate={}&endDate={}'.format(actors_, self.df['起始'][num], str(self.df['showtime'][num]).replace('00:00:00', ''))  # 搜索指数url
                response = json.loads(session.get(url=api_url, headers=self.headers, cookies=self.cookies, timeout=10, verify=False).text)
                if not response['data']:
                    logger.error('------------数据不存在--------------')
                    continue
                resp = json.loads(session.get(url=url, headers=self.headers, cookies=self.cookies).text)
                dit = {
                    '演员名称': actors_,
                    '搜索指数整体日均值': response['data']['generalRatio'][0]['all']['avg'],
                    '搜索指数移动日均值': response['data']['generalRatio'][0]['wise']['avg'],
                    '咨询指数日均值': resp['data']['index'][0]['generalRatio']['avg']
                }
                logger.info(dit)
                self.csv_writer.writerow(dit)
            with open('exist_news_url.txt', 'a', encoding='utf-8') as w:
                w.write('{}\n'.format(self.df['href'][num]))
            time.sleep(random.randint(2, 7))
            num += 1
        self.file.close()


if __name__ == '__main__':
    BdZs = BaiDuZs()
    BdZs.main()








