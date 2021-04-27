#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2020/2/18
# @Author  : GT
# 爬取搜狗平台搜索量

import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Mobile Safari/537.36"
}
url = """http://index.sogou.com/index/searchHeat?kwdNamesStr=%E8%83%BD%E6%BA%90%E4%BA%92%E8%81%94%E7%BD%91&timePeriodType=YEAR&dataType=SEARCH_ALL&queryType=INPUT"""


def get_html():
    res = requests.get(url, headers=headers)
    res.encoding = 'UTF-8'
    text = res.text
    print(res)
    with open('energy_internet/sougou-index.txt', 'w', encoding='UTF-8') as f:
        f.write(str(text))


get_html()
# parse html
with open('energy_internet/sougou-index.txt', 'r', encoding='UTF-8') as f:
    data = f.read()
begin = '"kwdId":1748974,'
end = ',"id"'
pat = re.compile(begin + '(.*?)' + end, re.S)
pv_and_date_string = pat.findall(data)
print(len(pv_and_date_string))
print(pv_and_date_string[0])
print(pv_and_date_string[1])
pv_and_date = []
for item in pv_and_date_string:
    date = item[-8:]
    pv_begin = '"pv":'
    pv_end = ',"'
    pat_pv = re.compile(pv_begin + '(.*?)' + pv_end)
    pv = pat_pv.findall(item)
    pv_and_date.append((date, pv[0]))
print(pv_and_date[0], len(pv_and_date))
buff = {}
used = []
for date, pv in pv_and_date:
    if date[:4] == '2020':
        if date in used:   # 部分数据出现了两次，需要去重
            continue
        used.append(date)
        if date[4:6] in buff:
            buff[date[4:6]] += int(pv)
        else:
            buff[date[4:6]] = int(pv)
print(buff)
print(len(used))
with open('energy_internet/sougou-index-parsed.txt', 'w') as f:
    for key in buff.keys():
        f.write(f'{key},{str(buff[key])}\n')


