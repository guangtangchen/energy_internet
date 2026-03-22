import csv
import requests
from bs4 import BeautifulSoup
import os
import re
import datetime
import random
import time

# 使用方法
# 1. 将收集（2026年时是手动在搜索页面截图，让豆包识别图片）到的新闻时间、标题和链接保存在一个csv文件中，格式如下：
# 时间,标题,链接
# 2019-01-01 12:00:00,新闻标题,http://news.example.com/article1
# 2019-01-02 13:30:00,另一个新闻标题,http://news.example.com/article2
# 2. 修改input_file和output_dir变量，分别指向输入的csv文件和输出的目录。
# 3. 运行脚本，脚本会自动爬取每条新闻的内容，并将其保存在output_dir目录下，文件名格式为：时间_标题.txt，例如：201

# 文件路径
input_file = r"D:\Desktop\能源互联网\中新网-搜索结果\中新网-新型电力系统-搜索结果.txt"
output_dir = r"E:\code\python\energy_internet\2025\临时文件\中新网新闻原文-新型电力系统"

os.makedirs(output_dir, exist_ok=True)

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # 跳过标题
    rows = list(reader)  # 读取所有行
    total = len(rows)
    
    for i, row in enumerate(rows, start=1):
        if len(row) == 3:
            time_str, title, url = row
        elif len(row) > 3:
            time_str = row[0]
            url = row[-1]
            title = ','.join(row[1:-1])
        else:
            print(f"跳过第{i}行，列数不足: {row}")
            continue
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
