# -*- coding: utf-8 -*-
import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re
import json
from bark_sdk import send_message
import os
import pytz


# 配置url
url = "https://rsshub.app/smzdm/keyword/shoei"
bark_url = "https://api.day.app/请输入你的链接/"
bark_title = 'shoei'


def handler(event, context):
    logger = logging.getLogger()
    logger.info('hello world')
    # 获取现在的时间
    current_time = datetime.now(pytz.timezone('Asia/Shanghai'))
    # 获取半小时前的时间
    previous_time = current_time - timedelta(minutes=30)

    # 将时间都转为字符串
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    previous_time_str = previous_time.strftime('%Y-%m-%d %H:%M:%S')

    print("现在时刻:{},30分钟前:{}".format(current_time_str, previous_time_str))

    # 获取rsshub的数据
    res_json_data = get_new_rsshub_smzdm(url)
    # 获取最新的数据的时间
    first_update_time = res_json_data[0]['local_time_str']

    # 将日期字符串转换为datetime对象
    date_first_update_time = datetime.strptime(
        first_update_time, "%Y-%m-%d %H:%M:%S")
    # 为日期时间对象添加时区信息
    date_first_update_time = pytz.utc.localize(date_first_update_time)
    print("previous_time:{},date_first_update_time:{}".format(
        previous_time, date_first_update_time))

    # 判断是否更新
    if previous_time > date_first_update_time:  # 最新的时间小于30分钟前
        print('没有更新')
    elif previous_time <= date_first_update_time:
        print('有更新')
        for i in res_json_data:
            # 遍历获取rsshub数据中的时间
            date_item_update_time = datetime.strptime(
                i['local_time_str'], "%Y-%m-%d %H:%M:%S")
            # 为日期时间对象添加时区信息
            date_item_update_time = pytz.utc.localize(date_item_update_time)

            # 如果时间大于30分钟前
            if date_item_update_time >= previous_time:
                print('有更新发消息')
                # 将日期时间对象转换为+8时区的字符串日期
                tz = pytz.timezone('Asia/Shanghai')
                date_str = date_item_update_time.astimezone(
                    tz).strftime("%Y-%m-%d %H:%M:%S")
                text = '{};{}'.format(
                    i['title'], date_str)
                send_message(bark_url, text, bark_title, sound='',
                             icon='', group='SMZDM', to_url=i['link'], copy='')
            else:
                break


# 获取数据
def get_new_rsshub_smzdm(url):
    payload = {}
    headers = {
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'host': 'rsshub.app'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.content)
    # 解析XML数据
    root = ET.fromstring(response.content)

    # 遍历XML结构并提取数据
    # 遍历每个项目(item)
    res_json_data = []
    for item in root.findall('.//item'):
        # 获取标题、日期和链接
        title = item.find('title').text
        pubDate = item.find('pubDate').text
        link = item.find('link').text
        # 将时间字符串转换为datetime对象
        gmt_time = datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S GMT")
        # 格式化为字符串
        local_time_str = gmt_time.strftime("%Y-%m-%d %H:%M:%S")
        # 打印信息
        print("标题:", title)
        print("时间:", local_time_str)
        print("链接:", link)
        json_item = {
            'title': title,
            'local_time_str': local_time_str,
            'link': link
        }
        res_json_data.append(json_item)
    return (res_json_data)


if __name__ == '__main__':
    handler(event=1, context=2)
