# -*- coding: utf-8 -*-
import scrapy
import os
from bs4 import BeautifulSoup
from weather.items import AirItem

class AirSpider(scrapy.Spider):
    name = 'air'
    allowed_domains = ['www.tianqihoubao.com']
    start_urls = []
    cities = ['nanjing', 'guangzhou', 'beijing', 'jiangmen', 'suzhou']
    
    for city in cities:
        for i in range(3):
            start_urls.append('http://www.tianqihoubao.com/aqi/' + city + '-2019' + str(i+10) + '.html')

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        
        cities_dict = {'nanjing': '南京', 'guangzhou': '广州', 'beijing': '北京', 'jiangmen': '江门', 'suzhou': '苏州'}
        airDict = ['质量等级', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

        AItems = []
        
        table = soup.find('table')
        data = table.find_all('tr')

        for index, item in enumerate(data):
            if index == 0:
                continue
            AItem = AirItem()
            cityname = response.request.url.split('/')[4][0:-12]
            AItem['city'] = cities_dict[cityname]
            AirData = item.find_all('td')

            date = AirData[0].string.strip().split('-')
            AItem['year'] = date[0]
            AItem['month'] = date[1]
            AItem['day'] = date[2]

            quality = AirData[1].string.strip()
            pm2_5 = AirData[4].string
            pm10 = AirData[5].string
            so2 = AirData[6].string
            no2 = AirData[7].string
            co = AirData[8].string
            o3 = AirData[9].string
            airList = [quality, pm2_5, pm10, so2, no2, co, o3]
            AItem['air'] = dict(zip(airDict, airList))
            yield AItem
