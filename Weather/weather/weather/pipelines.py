# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import codecs, json

class JsonPipeline(object):
    def process_item(self, item, spider):
        # JSON数据文件的保存位置
        filename = r'C:\Users\HHTti\Code\python\Weather\weather\weather\data\air.json'

        with open(filename, 'r', encoding='utf-8') as f:
            json_dict = json.loads(f.read())
        f.close()

        if item['city'] not in json_dict:
            json_dict[item['city']] = {}
        if item['year'] not in json_dict[item['city']]:
            json_dict[item['city']][item['year']] = {}
        if item['month'] not in json_dict[item['city']][item['year']]:
            json_dict[item['city']][item['year']][item['month']] = {}
        if item['day'] not in json_dict[item['city']][item['year']][item['month']]:
            json_dict[item['city']][item['year']][item['month']][item['day']] = {}

        json_dict[item['city']][item['year']][item['month']][item['day']] = dict(item['air'])

        with open(filename, 'w') as f:
            line = json.dumps(json_dict, ensure_ascii=False, indent=4) + '\n'
            f.write(line)
        f.close()
        return item

