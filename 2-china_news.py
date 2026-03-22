import os
import requests
import json
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup

# 目标关键词和时间范围
KEYWORD = '能源互联网'
START_DATE = '2025-01-01'
END_DATE = '2025-12-31'
SAVE_DIR = os.path.join('2025', '临时文件', '中新网新闻原文'+KEYWORD+datetime.now().strftime('%Y%m%d%H%M%S'))

# 测试模式标志
TEST_MODE = False #true只抓取1-2条先看看效果，False抓全量
# TEST_MODE = True #true只抓取1-2条先看看效果，False抓全量


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
        if TEST_MODE and len(all_news) >= 2:
            break
    print(f'已抓取第{page}页，共{len(all_news)}条')
    if TEST_MODE and len(all_news) >= 2:
        break
    sleep(0.5)  # 防止被封

# 清洗文件名
def clean_filename(s):
    import re
    s = re.sub(r'[\\/:*?"<>|]', '', s)  # 去除非法字符
    s = s.strip().replace(' ', '_')
    return s[:50]  # 最多保留50字符，防止过长

# 抓取新闻原文
for idx, news in enumerate(all_news):
    url = news['url']
    title = news['title']
    pubtime = news['pubtime']
    if not url:
        continue
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        # 自动检测编码，优先用apparent_encoding
        resp.encoding = resp.apparent_encoding or resp.encoding
        html = resp.text
        # 用BeautifulSoup提取正文
        soup = BeautifulSoup(html, 'html.parser')
        content_tag = soup.find('div', class_='left_zw')
        if content_tag is None:
            content_tag = soup.find('div', class_='content')
        if content_tag is None:
            # 兼容更多结构
            for cls in ['article-content', 'article', 'articleBody', 'main-content', 'content-main']:
                content_tag = soup.find('div', class_=cls)
                if content_tag:
                    break
        if content_tag is None:
            print(f'未找到正文: {url}')
            continue
        content = content_tag.get_text(separator='\n', strip=True)
        # 若内容异常短，尝试用gbk解码
        if len(content.strip()) < 10:
            try:
                html = resp.content.decode('gbk', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                content_tag = soup.find('div', class_='left_zw')
                if content_tag is None:
                    content_tag = soup.find('div', class_='content')
                if content_tag is None:
                    for cls in ['article-content', 'article', 'articleBody', 'main-content', 'content-main']:
                        content_tag = soup.find('div', class_=cls)
                        if content_tag:
                            break
                if content_tag:
                    content = content_tag.get_text(separator='\n', strip=True)
            except Exception as e2:
                print(f'GBK解码失败: {url}, 错误: {e2}')
        # 文件名：发布日期_序号_标题.txt
        date_str = pubtime.split(' ')[0].replace('-', '')
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
    except Exception as e:
        print(f'抓取失败: {url}, 错误: {e}')

print('全部完成')
