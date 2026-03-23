import csv
import requests
from bs4 import BeautifulSoup
import os
import re
import datetime
import random
import time

# 文件路径
input_file = r"D:\Desktop\能源互联网-手工保存数据\人民网-搜索结果\人民网-能源互联网-搜索结果.txt"
output_dir = r"E:\code\python\energy_internet\2025\临时文件\人民网新闻原文-能源互联网"

os.makedirs(output_dir, exist_ok=True)

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # 跳过表头
    rows = list(reader)  # 读取所有行
    total = len(rows)
    
    for i, row in enumerate(rows, start=1):
        if len(row) < 3:
            print(f"跳过第{i}行，列数不足: {row}")
            continue
        time_str = row[0]
        title = row[1]
        url = row[2]
        print(f"正在处理第 {i}/{total} 条新闻: {title}")
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
            content_div = soup.find('div', id='content')
            if not content_div:
                content_div = soup.find('div', class_='content')
            if content_div:
                content = content_div.get_text()
            else:
                content = "内容未找到"
        except Exception as e:
            content = f"爬取失败: {str(e)}"
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(f"标题: {title}\n")
            out_f.write(f"时间: {time_str}\n")
            out_f.write(f"链接: {url}\n\n")
            out_f.write(content)
        
        # 随机sleep
        time.sleep(random.uniform(0.5, 1))
