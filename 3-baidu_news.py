import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

# 搜索关键词和时间范围
KEYWORD = '能源互联网'
START_DATE = '2025-01-01'
END_DATE = '2025-12-31'
SAVE_DIR = os.path.join('2025', '临时文件', '百度新闻原文'+KEYWORD+datetime.now().strftime('%Y%m%d%H%M%S'))
TEST_MODE = True  # True只抓取1-2条，False抓全量

os.makedirs(SAVE_DIR, exist_ok=True)

# 清洗文件名
def clean_filename(s):
    import re
    s = re.sub(r'[\\/:*?"<>|]', '', s)
    s = s.strip().replace(' ', '_')
    return s[:50]

# 百度新闻搜索分页参数
# pn=0,10,20...，每页10条
# 时间过滤用ct=1&bt=开始时间戳&lt=结束时间戳
import time
start_ts = int(time.mktime(time.strptime(START_DATE, '%Y-%m-%d')))
end_ts = int(time.mktime(time.strptime(END_DATE, '%Y-%m-%d')))

base_url = 'https://www.baidu.com/s'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

all_news = []
for page in range(0, 1000):  # 最多100页，实际遇到无数据会break
    params = {
        'rtt': '1',
        'bsst': '1',
        'cl': '2',
        'tn': 'news',
        'rsv_dl': 'ns_pc',
        'word': KEYWORD,
        'pn': page * 10,
        'ct': '1',
        'bt': start_ts,
        'et': end_ts
    }
    resp = requests.get(base_url, params=params, headers=headers)
    if resp.status_code != 200:
        print(f'第{page+1}页获取失败')
        break
    soup = BeautifulSoup(resp.text, 'html.parser')
    news_items = soup.find_all('div', class_='result')
    if not news_items:
        news_items = soup.find_all('div', class_='result-op')
    if not news_items:
        print(f'第{page+1}页无新闻，提前结束')
        break
    for item in news_items:
        a = item.find('a')
        if not a:
            continue
        title = a.get_text(strip=True)
        url = a.get('href')
        # 发布时间
        pubtime = ''
        time_tag = item.find('span', class_='c-color-gray2')
        if time_tag:
            pubtime = time_tag.get_text(strip=True)
        all_news.append({'title': title, 'url': url, 'pubtime': pubtime})
        if TEST_MODE and len(all_news) >= 2:
            break
    print(f'已抓取第{page+1}页，共{len(all_news)}条')
    if TEST_MODE and len(all_news) >= 2:
        break
    sleep(0.5)

# 抓取新闻原文
for idx, news in enumerate(all_news):
    url = news['url']
    title = news['title']
    pubtime = news['pubtime']
    content = ''
    if url:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.encoding = resp.apparent_encoding or resp.encoding
            html = resp.text
            soup = BeautifulSoup(html, 'html.parser')
            # 常见正文div
            for cls in ['article', 'main-content', 'content', 'article-content', 'left_zw', 'articleBody', 'content-main']:
                content_tag = soup.find('div', class_=cls)
                if content_tag:
                    content = content_tag.get_text(separator='\n', strip=True)
                    break
            if not content:
                # 退而求其次，抓p标签拼接
                ps = soup.find_all('p')
                if ps:
                    content = '\n'.join([p.get_text(strip=True) for p in ps])
        except Exception as e:
            print(f'正文抓取失败: {url}, 错误: {e}')
    # 文件名
    date_str = pubtime.split(' ')[0].replace('-', '') if pubtime else 'unknown'
    safe_title = clean_filename(title)
    filename = f'{date_str}_{idx+1}_{safe_title}.txt'
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'{title}\n{url}\n{pubtime}\n\n{content}')
    print(f'保存: {filepath}')
    sleep(0.2)
    if TEST_MODE and idx >= 1:
        print('测试模式，仅抓取前2条，提前结束。')
        break

print('全部完成')
