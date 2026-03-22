import requests
import json

# 1. 接口基础信息
url = "http://search.people.cn/search-platform/front/search"

# 2. 请求头（完全复刻浏览器的请求头）
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

# 3. 请求参数（完全对应Payload中的字段）
payload = {
    "belongsId": [],
    "endTime": 0,
    "hasContent": True,
    "hasTitle": True,
    "isFuzzy": False,
    "key": "新型电力系统",
    "limit": 10,
    "page": 50,
    "sortType": 0,
    "startTime": 0,
    "type": 0
}

def search_news():
    try:
        # 4. 发送POST请求（json参数会自动设置Content-Type并序列化）
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=10  # 设置超时时间，避免卡死
        )

        # 5. 检查响应状态码
        if response.status_code == 200:
            print("✅ 请求成功！状态码：", response.status_code)
            print("\n" + "="*50 + "\n")

            # 6. 解析JSON响应并格式化打印
            try:
                response_data = response.json()
                print("📄 响应数据（格式化后）：")
                print(json.dumps(response_data, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                print("⚠️ 响应不是标准JSON格式，原始内容：")
                print(response.text)
        else:
            print(f"❌ 请求失败！状态码：{response.status_code}")
            print("响应内容：", response.text)

    except requests.exceptions.RequestException as e:
        print(f"🚨 请求发生异常：{str(e)}")

if __name__ == "__main__":
    search_news()