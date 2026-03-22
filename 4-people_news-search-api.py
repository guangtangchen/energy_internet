import requests
import json
import csv
import time
import random
from datetime import datetime

# 本文件的功能：爬取人民网新闻搜索接口的数据，提取时间、标题、链接，保存到CSV文件中

# 请求配置
url = "http://search.people.cn/search-platform/front/search"

# 请求头：建议在页面里打开检查，看下search接口实际的请求头，保持一致
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
    "Content-Type": "application/json;charset=UTF-8",
    "Cookie": "_jsluid_h=71bdefb8e521166c1450ceff9f7e2a84; sso_c=0; sfr=1",
    "Host": "search.people.cn",
    "Origin": "http://search.people.cn",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://search.people.cn/s?keyword=%E6%96%B0%E5%9E%8B%E7%94%B5%E5%8A%9B%E7%B3%BB%E7%BB%9F&st=0&_=1774196314233",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0 Safari/537.36"
}

# 基础请求参数：建议在页面里打开检查，看下search接口实际payload
base_payload = {
    "belongsId": [],
    "endTime": 0,
    "hasContent": True,
    "hasTitle": True,
    "isFuzzy": False,
    "key": "新型电力系统", # 搜索的关键词
    "limit": 10, # 每页数量，不要改
    "sortType": 0,
    "startTime": 0,
    "type": 0
}

# 查询的页码范围：根据实际情况调整。查出来的数据可能包含非本年的数据，自己删一下
start_page = 40
end_page = 300

# CSV文件配置
csv_filename  = base_payload['key']+"people_news_urls.csv"
csv_header = ["时间", "标题", "链接"]


def timestamp_to_datetime(timestamp_ms):
    """
    将毫秒级时间戳转换为指定格式的日期字符串
    :param timestamp_ms: 毫秒时间戳
    :return: 格式化的时间字符串，如 2025-12-05 11:26:41
    """
    try:
        # 转换为秒级时间戳
        timestamp_s = timestamp_ms / 1000
        # 格式化时间
        return datetime.fromtimestamp(timestamp_s).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ""


def init_csv():
    """初始化CSV文件，写入表头"""
    with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)


def append_to_csv(data_row):
    """追加数据到CSV文件"""
    with open(csv_filename, "a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_row)


def fetch_page_data(page_num):
    """
    获取指定页码的数据
    :param page_num: 页码
    :return: 该页的记录列表，失败返回空列表
    """
    # 复制基础参数并更新页码
    payload = base_payload.copy()
    payload["page"] = page_num

    try:
        # 发送POST请求
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=30  # 设置超时时间
        )

        # 检查请求是否成功
        response.raise_for_status()

        # 解析JSON响应
        response_data = response.json()

        # 提取records数组
        records = response_data.get("data", {}).get("records", [])

        print(f"第 {page_num} 页: 获取到 {len(records)} 条记录")
        return records

    except requests.exceptions.RequestException as e:
        print(f"第 {page_num} 页请求出错: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"第 {page_num} 页JSON解析出错: {e}")
        return []
    except Exception as e:
        print(f"第 {page_num} 页处理出错: {e}")
        return []


def main():
    # 初始化CSV文件
    init_csv()
    print(f"初始化CSV文件: {csv_filename}")

    # 配置爬取范围
    total_records = 0

    # 遍历页码爬取数据
    for page in range(start_page, end_page + 1):
        # 获取当前页数据
        records = fetch_page_data(page)

        if not records:
            print(f"第 {page} 页无数据，继续下一页")
            # 依然添加延时，避免被识别为爬虫
            sleep_time = random.uniform(0.5, 1.0)
            time.sleep(sleep_time)
            continue

        # 处理当前页的每条记录
        for record in records:
            # 提取字段
            display_time_ms = record.get("displayTime", 0)
            title = record.get("title", "")
            url_link = record.get("url", "")

            # 格式化时间
            display_time = timestamp_to_datetime(display_time_ms)

            # 组装数据行
            row = [display_time, title, url_link]

            # 追加到CSV文件
            append_to_csv(row)

            # 打印提取的信息
            print(f"  - 时间: {display_time} | 标题: {title[:50]}... | 链接: {url_link}")

            total_records += 1

        # 随机延时 0.5-1秒
        sleep_time = random.uniform(0.5, 1.0)
        print(f"第 {page} 页处理完成，等待 {sleep_time:.2f} 秒...\n")
        time.sleep(sleep_time)

    # 爬取完成统计
    print("=" * 80)
    print(f"爬取完成！")
    print(f"爬取范围: 第 {start_page} 页 到 第 {end_page} 页")
    print(f"总共提取记录数: {total_records} 条")
    print(f"数据已保存至: {csv_filename}")


if __name__ == "__main__":
    main()