#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @Version : 1.0
# @Time    : 2020/2/18
# @Author  : GT
# 爬取百度平台搜索量

import requests
import re

date = [('1-1', '1-31'),
        ('2-1', '2-28'),
        ('3-1', '3-31'),
        ('4-1', '4-30'),
        ('5-1', '5-31'),
        ('6-1', '6-30'),
        ('7-1', '7-31'),
        ('8-1', '8-31'),
        ('9-1', '9-30'),
        ('10-1', '10-31'),
        ('11-1', '11-30'),
        ('12-1', '12-31')]
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Mobile Safari/537.36",
    "Cookie":"""PSTM=1580633926; BIDUPSID=09542EE6BDD409937A6DC1106C42FB4B; BAIDUID=03640D8892CB0BF5DF03E2EAFC81C5EA:FG=1; BDUSS=mVVSXdPSnBwVEJDU1laaUJBYS1GZEJsUnVqTHR2Nk5ydlh-RlE0RkhjeUJkV0plRVFBQUFBJCQAAAAAAAAAAAEAAACIg~c9s8K54szDZmx5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIHoOl6B6Dped; bdshare_firstime=1581059829256; _ga=GA1.2.1134945114.1581060110; _gcl_aw=GCL.1581755876.Cj0KCQiAn8nuBRCzARIsAJcdIfNFkHtbPCuSWcAWdin6z4KSlOGTQUzbBvRwQIqXnDfCNfhYMym22ucaAn1nEALw_wcB; _gac_UA-138572523-1=1.1581755877.Cj0KCQiAn8nuBRCzARIsAJcdIfNFkHtbPCuSWcAWdin6z4KSlOGTQUzbBvRwQIqXnDfCNfhYMym22ucaAn1nEALw_wcB; __xsptplus861=861.1.1581755755.1581755876.3%233%7Cwww.google.com%7C%7C%7C%7C%23%23a0efy11CB_we588zWCElKyh8DBZBav_1%23; H_WISE_SIDS=141911_132921_128698_141845_142080_142209_142064_142113_135846_141001_128146_138596_140853_141915_133995_138878_137979_141199_140173_131247_137745_138165_107314_138883_140259_141838_140201_140592_138585_141650_140989_141901_140114_141742_140327_140579_133847_140066_134046_141807_131423_140367_137703_141102_110085_141941_127969_140593_139549_139886_140995_138425_138941_141190_142157_141925; ZD_ENTRY=google; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1581059809,1581061912,1582017849; bdindexid=cob3aghemj5nh4v7pq6o5elkk5; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1582017861; RT="z=1&dm=baidu.com&si=figs6z6ymq&ss=k6rol58u&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=y8&ul=6g35g&hd=6g368"; __yjsv5_shitong=1.0_7_2ce1ea0e32e72bd6f21b8ec1eaea5addefa6_300_1582028693810_222.181.204.165_1211ba1d; yjs_js_security_passport=222ae935c33a5e82a3a2bcfdc3bfa1c4488859ba_1582028694_js"""
}
for start_date, end_date in date:
    url = f"http://index.baidu.com/api/SearchApi/index?area=0&word=能源互联网&startDate=2019-{start_date}&endDate=2019-{end_date}"
    response = requests.get(url, headers=headers)
    response.encoding = 'UTF-8'
    text = response.text
    print(text)
    with open(f'energy_internet/{start_date}.txt', 'w') as f:
        f.write(str(text))
    begin = '"all":{"avg":'
    end = ',"yoy":'
    pat = re.compile(begin + '(.*?)' + end, re.S)
    answer = pat.findall(str(text))
    print(start_date, answer)
    with open('energy_internet/baidu_index_all.txt', 'a') as f:
        days = end_date[-2:]
        sum = str(int(days)*int(answer[0]))
        f.write(f"{start_date[:-2]},{answer[0]},{days},{sum}\n")


