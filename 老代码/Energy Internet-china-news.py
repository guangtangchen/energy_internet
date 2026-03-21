#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2020/2/19
# @Author  : dongyouyuan
#
# 爬取中新网相关新闻
import re
import requests
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Mobile Safari/537.36"
}


def main_get_words_num():
    buff_all = {}
    with open('energy_internet/china_news_time_and_href.txt', 'r') as f:
        data = f.read().split('{{')
        date_and_href = []
        for item in data:
            date_and_href.append(item.split('@@@@'))
        print(len(date_and_href), date_and_href[0])
    count1 = 0
    for item in date_and_href:
        count1 += 1
        try:
            date, href = item[0], item[1]
            if date[:4] == '2019':
                print(f'获取第{str(count1)}个链接中', href)
                words_num_single_href = parse_single_href(href)
                if date[:7] in buff_all:
                    buff_all[date[:7]] = add_two_dicts(buff_all[date[:7]], words_num_single_href)
                else:
                    buff_all[date[:7]] = add_two_dicts({}, words_num_single_href)
        except:
            print('此链接无效', item)
    with open('energy_internet/china_news_words_num.txt', 'w') as f:
        f.write('month,')
        for word in buff_all['2019-12'].keys():
            f.write(f'{word},')
        f.write('\n')
        for month in buff_all.keys():
            f.write(month+',')
            for word in buff_all[month].keys():
                f.write(str(buff_all[month][word])+',')
            f.write('\n')
    print(buff_all)
    print('done')


def parse_single_href(href):
    try:
        res = requests.get(href, headers=headers)
        res.encoding = 'UTF-8'
        r_text = res.text
    except:
        print('链接获取失败', href)
        r_text = ''
    per_item = dict()
    per_item['key_1_dnhb'] = r_text.count("多能互补")
    per_item['key_2_rxdd'] = r_text.count("柔性输电")
    per_item['key_3_zhny'] = r_text.count("综合能源")
    per_item['key_4_qn'] = r_text.count("氢能")
    per_item['key_5_ddqc'] = r_text.count("电动汽车")
    print(per_item['key_5_ddqc'])
    per_item['key_6_fbsny'] = r_text.count("分布式能源")
    per_item['key_7_ww'] = r_text.count("微网")
    per_item['key_8_xqcgljxy'] = r_text.count("需求侧管理及响应")
    per_item['key_9_cn'] = r_text.count("储能")
    per_item['key_10_cchp'] = r_text.count("CCHP")
    per_item['key_11_rldc'] = r_text.count("燃料电池")
    per_item['key_12_zhgl'] = r_text.count("综合管廊")
    per_item['key_13_nyhlw'] = r_text.count("能源物联网")
    per_item['key_14_nydsj'] = r_text.count("能源大数据")
    per_item['key_15_dljy'] = r_text.count("电力交易")
    per_item['key_16_nx'] = r_text.count("能效")
    per_item['key_17_jn'] = r_text.count("节能")
    per_item['key_18_xndc'] = r_text.count("虚拟电厂")
    per_item['key_19_zhnyxt'] = r_text.count("综合能源系统")
    per_item['key_20_qkl'] = r_text.count("区块链")
    per_item['key_21_nllyq'] = r_text.count("能量路由器")
    per_item['key_22_fbsjy'] = r_text.count("分布式交易")
    per_item['key_23_dnl'] = r_text.count("多能流")
    return per_item.copy()


def add_two_dicts(d1, d2):
    if not d1:
        return d2.copy()
    for key in d1.keys():
        d2[key] += d1[key]
    return d2.copy()


#   获取每月新闻数量
def get_parse_url(text):
    # parse
    begin = '''class="news_title">
											<a href="'''
    end = '"'
    pat = re.compile(begin + '(.*?)' + end, re.S)
    href = pat.findall(text)
    date = re.findall('\d\d\d\d-\d\d-\d\d', text)
    if date[0] == '2009-02-04':
        date.pop(0)
    date_and_href = []
    for i in range(len(href)):
        try:
            date_and_href.append((href[i], date[i]))
            date_all.append(date[i])
        except:
            print('date and href len diff:', len(date), len(href))
    print("本页面获取的条目数量：",len(date_and_href))
    with open('energy_internet/china_news_time_and_href.txt', 'a') as f:
        for href, date in date_and_href:
            f.write(f"{date}@@@@{href}{{{{")


def main_get_news_num_per_month():
    files = os.listdir('energy_internet/china')
    for file in files:
        if file.split('.')[-1] != 'html':
            continue
        with open('energy_internet/china/'+file, 'r', encoding='UTF-8') as f:
            data = f.read()
            get_parse_url(data)
    buff = {}
    print('日期总条数', len(date_all))
    count = 0
    for date in date_all:
        if date[:4] == '2019':
            count += 1
            if date[:8] in buff:
                buff[date[:8]] += 1
            else:
                buff[date[:8]] = 1
    with open('energy_internet/china_news_num.txt', 'w') as f:
        for month in buff.keys():
            f.write(f"{month},{str(buff[month])}\n")
    print(buff)


date_all = []
# main_get_news_num_per_month()
main_get_words_num()