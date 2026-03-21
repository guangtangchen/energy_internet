import os
import requests
import json
from datetime import datetime
from time import sleep

# 目标关键词和时间范围
KEYWORD = '能源互联网'
START_DATE = '2025-01-01'
END_DATE = '2025-12-31'
SAVE_DIR = os.path.join('2025', '临时文件', '中新网新闻原文')

# 创建保存目录
os.makedirs(SAVE_DIR, exist_ok=True)

# 搜索API参数
BASE_URL = 'https://sou.chinanews.com.cn/search.do'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

# 获取总页数
params = {
    'q': KEYWORD,
    'startdate': START_DATE,
    'enddate': END_DATE,
    'page': 1
}
resp = requests.get(BASE_URL, params=params, headers=HEADERS)
if resp.status_code != 200:
    print('无法获取搜索结果首页')
    exit(1)
# 提取docArr和totalNum
html = resp.text
start = html.find('var docArr = ')
if start == -1:
    print('未找到docArr')
    exit(1)
start += len('var docArr = ')
end = html.find(';', start)
docArr_str = html[start:end].strip()
docArr = json.loads(docArr_str)
# 获取总条数
start_total = html.find('var totalNum = ')
if start_total == -1:
    print('未找到totalNum')
    exit(1)
start_total += len('var totalNum = ')
end_total = html.find(';', start_total)
totalNum = int(html[start_total:end_total].strip())
pageSize = 10
pageCount = (totalNum + pageSize - 1) // pageSize
print(f'共{totalNum}条，{pageCount}页')

# 获取所有新闻链接
all_news = []
for page in range(1, pageCount + 1):
    params['page'] = page
    resp = requests.get(BASE_URL, params=params, headers=HEADERS)
    if resp.status_code != 200:
        print(f'第{page}页获取失败')
        continue
    html = resp.text
    start = html.find('var docArr = ')
    if start == -1:
        print(f'第{page}页未找到docArr')
        continue
    start += len('var docArr = ')
    end = html.find(';', start)
    docArr_str = html[start:end].strip()
    try:
        docArr = json.loads(docArr_str)
    except Exception as e:
        print(f'第{page}页docArr解析失败: {e}')
        continue
    for item in docArr:
        all_news.append({
            'title': item.get('title', ''),
            'url': item.get('url', ''),
            'pubtime': item.get('pubtime', '')
        })
    print(f'已抓取第{page}页，共{len(all_news)}条')
    sleep(0.5)  # 防止被封

# 抓取新闻原文
for idx, news in enumerate(all_news):
    url = news['url']
    title = news['title']
    pubtime = news['pubtime']
    if not url:
        continue
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f'新闻{url}获取失败')
            continue
        html = resp.text
        # 尝试提取正文
        # 常见结构：<div class="left_zw">...</div>
        start = html.find('<div class="left_zw">')
        if start == -1:
            start = html.find('<div class="content">')
        if start == -1:
            print(f'未找到正文: {url}')
            continue
        end = html.find('</div>', start)
        content_html = html[start:end]
        # 去除HTML标签
        import re
        content = re.sub('<[^<]+?>', '', content_html)
        # 文件名：发布日期_序号.txt
        date_str = pubtime.split(' ')[0].replace('-', '')
        filename = f'{date_str}_{idx+1}.txt'
        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f'{title}\n{url}\n{pubtime}\n\n{content.strip()}')
        print(f'保存: {filepath}')
        sleep(0.2)
    except Exception as e:
        print(f'抓取失败: {url}, 错误: {e}')

print('全部完成')

