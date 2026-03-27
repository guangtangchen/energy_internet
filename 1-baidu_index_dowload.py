
def decrypt(t, e):
    n = list(t)
    i = list(e)
    a = {}
    result = []
    ln = int(len(n) / 2)
    start = n[ln:]
    end = n[:ln]
    for j, k in zip(start, end):
        a.update({k: j})
    for j in e:
        result.append(a.get(j))
    resp_str = ''.join(result)

    return resp_str.split(",")

# 百度指数网站的数据是收费的，前端看到的也是加密后的，需要解密
if __name__ == '__main__':
    # 1. 进入百度指数网站"https://index.baidu.com/v2/index.html#/"，打开浏览器检查，在网页选择对应的关键词和时间范围（可以直接选一年，目前看搜索一年范围也能拿到天级的数据）
    # 2. 找到index请求（不是getFeedIndex）的response，复制uniqid，形如"6a4154ccfa4aa05da96ac7db015e7225"，不要关闭本窗口，稍后还需要使用本窗口的数据
    # 3. 换秘钥，用2的uniqid替换url(见后)中的uniqid并在浏览器访问新窗口，http://index.baidu.com/Interface/ptbk?uniqid=412e251ec0ad8e1dcd1c91d914869471
    # 4. 2到3要快，url只有约1分钟有效期
    # 5. 用3的response的data字段值作为秘钥，替换下面的key
    # 6. 用2的resp中的data.userindexs.all.data替换下面的data，即密文
    key = 'gs62dxSGQhpH9q4-7.43150,68+%92'
    data = """x42Qx4pQxdSQQxxsQx4SQx2xQx4qQx42QxdxQx4sQx4GQx4pQpGQxdhQx4dQxddQx4GQx4hQxxsQx44QQxxpQxxhQhdQxxsQQQxxhQQQQQQQx4sQx4GQxddQx4sQx4xQx4pQxdsQx4hQx2pQxdxQQx4dQx4hQx4sQx4xQx2xQxd2QhSQx4xQx4hQxdsQxdpQx24QxdGQxxsQx4dQxdqQxdGQxdqQxdGQxdqQx4sQhsQxddQxd4QxdqQxdqQxdxQxxqQx4sQxdqQxd4Qx4qQxdhQxdhQx44QxdGQx2dQx2xQx4hQxd2QxdhQxd2QxxhQx4hQhhQxdGQxdqQx4GQQx42QxdxQxddQxd2Qxd2QhxQhSQxdGQx42QxdGQxdsQxdGQxdhQQQx4sQx4hQxdqQxdhQx44QxxhQx2xQxd4Qxd4Qxd4QhdQQx4dQQhhQx4GQxS4Qx4xQx42QhhQQx4sQx4dQx2pQx2SQx4qQx44Qx4xQxdxQxdGQx4SQx4pQxd4Qx42Qx44Qx4pQx4xQxdGQx4sQx4pQxxhQQQxdGQxddQxdxQx4sQx42Qx4hQxd4Qx4SQxd2QxdhQx4hQx42QQxdsQx4qQxd4Qx22Qx2hQx44QxxqQx22QxdsQxspQxqsQxq2Q4G2Q4xGQxpsQxsGQxpqQxhdQxSpQxdqQxddQxdpQxqqQxdhQxxhQx4hQxxpQx4SQx4hQxdGQx4dQx42QxdhQx4hQxdGQxd2QxdsQxdxQx2xQxdxQx4sQQx42QQQxxhQx4pQxdSQx4pQxdGQx4sQSqQx4dQx4pQQQx4pQx44Qxd4Qx4sQx44Qx44Qx44Qx44QxxqQx4hQQx4xQx4GQxxpQSqQhxQx42QxdxQQQx4hQx4dQx42QxdSQx42QQQx4dQxdSQxSSQxh4Qx4hQx4SQhqQxxpQx4hQx42QSqQx4hQx44Qx44Qx42QxdGQx4dQxddQxd2Qx42Qx4GQx42Qx4SQx4xQhxQQQxxpQxxpQQQQxdGQx4SQx4GQx4GQxdxQx2dQQx4sQx4qQSqQx42Qx44Qx4GQx4SQx42QSqQhhQx42Qx4qQx4GQx4sQxddQx4GQQQxdxQhxQxd2Qx4pQx4sQhxQx4xQxdGQx4sQsGQx4qQx4xQx24QhxQQhdQx4GQx4qQxsxQx2xQx4sQx4hQx4sQx4hQx4pQxxpQx4GQx4qQx44QQh2Qx4sQx4qQx2dQQx42Qxd4Qx4dQhxQx42Qx4GQx44Qx42Qx4xQx42QhdQx4GQhdQx42Qx44QhxQx4qQxd4QhsQSqQQx42QhdQx44"""
    resp = decrypt(key, data)

    # 打印解密后的数组长度，以及全部元素
    print(f"解密后的数组长度: {len(resp)}")
    print("解密后的数组元素:", resp)


    from datetime import datetime, timedelta
    import csv

    # 生成2025年1月1日到2025年12月31日的日期列表
    preYear = datetime.now().year - 1
    start_date = datetime(preYear,1, 1)
    end_date = datetime(preYear,12, 31)
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime('%Y%m%d'))
        current_date += timedelta(days=1)

    # 检查resp长度和日期长度是否一致
    if len(resp) != len(date_list):
        print(f"Warning: 日期数量({len(date_list)})与数据数量({len(resp)})不一致！")

    # 写入CSV文件
    with open('baidu_index.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['日期', '数值'])
        for date, value in zip(date_list, resp):
            writer.writerow([date, value if value != '' else '0'])
    print(f"已生成 baidu_index.csv，包含{min(len(date_list), len(resp))}条数据。")

