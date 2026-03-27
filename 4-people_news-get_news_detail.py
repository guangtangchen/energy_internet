import csv
from xmlrpc.client import FastParser

import requests
from bs4 import BeautifulSoup
import os
import re
import datetime
import random
import time

# 文件路径
input_file = r"D:\Desktop\能源互联网-手工保存数据\人民网-搜索结果\人民网-新型电力系统-搜索结果.txt"
output_dir = r"E:\code\python\energy_internet\2025\临时文件\人民网新闻原文-新型电力系统"

# 测试模式：只处理前5条
test_mode = True
test_limit = 5

os.makedirs(output_dir, exist_ok=True)

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # 跳过表头
    rows = list(reader)  # 读取所有行
    if test_mode:
        rows = rows[:test_limit]
    total = len(rows)
    
    for i, row in enumerate(rows, start=1):
        if len(row) < 3:
            print(f"跳过第{i}行，列数不足: {row}")
            continue
        time_str = row[0]
        title = row[1]
        url = row[2]
        # print(f"正在处理第 {i}/{total} 条新闻: {title}")
        # 格式化时间
        try:
            time_obj = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            time_obj = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        formatted_time = time_obj.strftime('%Y%m%d_%H%M')
        # 清理标题，去掉特殊字符
        clean_title = re.sub(r'[\/:*?"<>|]', '', title)
        filename = f"{formatted_time}_{clean_title}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # 爬取内容
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            # 提取内容
            content_div = soup.find('div', class_='content')
            if not content_div:
                content_div = soup.find('div', class_='article-content')
            if not content_div:
                content_div = soup.find('div', class_='news-content')
            if not content_div:
                content_div = soup.find('div', class_='box_con')
            if not content_div:
                content_div = soup.find('div', id='content')
            if content_div:
                content = content_div.get_text()
            else:
                # 尝试获取所有p标签
                paragraphs = soup.find_all('p')
                content = '\n'.join([p.get_text() for p in paragraphs])
                if not content:
                    content = "内容未找到"
        except Exception as e:
            content = f"爬取失败: {str(e)}"
        
        # 计算汉字数量
        chinese_count = sum(1 for char in content if '\u4e00' <= char <= '\u9fff')
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(f"标题: {title}\n")
            out_f.write(f"时间: {time_str}\n")
            out_f.write(f"链接: {url}\n\n")
            out_f.write(content)
        
        print(f"正在处理第 {i}/{total} 条新闻: (汉字数: {chinese_count}) {title} - {url}")
        
        # 随机sleep
        time.sleep(random.uniform(0.5, 1))
