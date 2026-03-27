import os
import re
import csv
from collections import defaultdict


def extract_date_from_filename(filename):
    """从文件名提取前8位数字作为日期"""
    date_pattern = re.compile(r'^\d{8}')
    match = date_pattern.match(filename)
    return match.group() if match else ""


def count_keyword_in_file(file_path, keywords, encoding='utf-8'):
    """统计单个TXT文件中各关键词的出现次数（精准中文匹配）"""
    keyword_count = {kw: 0 for kw in keywords}
    try:
        # 读取文件：保留原始格式，忽略编码错误
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()

        for keyword in keywords:
            # 核心：无边界精准匹配中文关键词，避免漏统计
            pattern = re.compile(re.escape(keyword))
            keyword_count[keyword] = len(pattern.findall(content))

    except Exception as e:
        print(f"⚠️ 读取文件 {file_path} 出错: {str(e)}")
        # 出错时计数设为-1，便于识别异常文件
        keyword_count = {kw: -1 for kw in keywords}
    return keyword_count


def batch_process_files(folder_path, keywords, encoding='utf-8'):
    """批量处理文件，按日期+关键词汇总当日总次数，同时统计当日新闻数量"""
    # 存储：日期 → 关键词 → 当日总次数
    date_kw_total = defaultdict(lambda: defaultdict(int))
    # 存储：日期 → 当日新闻数量（TXT文件数）
    date_file_count = defaultdict(int)
    debug_date = '20250119'
    debug_kw = '电动汽车'

    # 校验文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"❌ 错误：文件夹 {folder_path} 不存在！")
        return date_kw_total, date_file_count

    # 筛选所有txt文件
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    print(f"📂 找到 {len(txt_files)} 个TXT文件，开始处理...")

    for filename in txt_files:
        date_str = extract_date_from_filename(filename)
        if not date_str:
            print(f"⚠️ 文件 {filename} 无有效日期，跳过")
            continue

        # 更新日期文件数（新闻数量）
        date_file_count[date_str] += 1

        # 拼接文件路径并统计关键词
        file_path = os.path.join(folder_path, filename)
        file_kw_count = count_keyword_in_file(file_path, keywords, encoding)

        # 汇总到当日总次数（跳过异常文件的-1计数）
        for kw in keywords:
            if file_kw_count[kw] != -1:
                date_kw_total[date_str][kw] += file_kw_count[kw]

    # 打印20250119调试信息
    print(f"\n📈 20250119 调试汇总：")
    print(f"   该日期下的新闻数量（文件数）：{date_file_count.get(debug_date, 0)}")
    print(f"   「{debug_kw}」当日总次数：{date_kw_total.get(debug_date, {}).get(debug_kw, 0)}")
    return date_kw_total, date_file_count


def validate_specific_data(date_kw_total, target_date='20250119', target_kw='电动汽车', expected=3):
    """校验20250119电动汽车的统计结果是否为3"""
    actual = date_kw_total.get(target_date, {}).get(target_kw, 0)
    print(f"\n🔍 数据校验：{target_date} 「{target_kw}」")
    print(f"   预期值：{expected} | 实际值：{actual}")
    if actual == expected:
        print(f"   ✅ 校验通过！统计结果准确")
    else:
        print(f"   ❌ 校验失败！请检查文件编码或关键词匹配")
    return actual == expected


def save_to_csv(date_kw_total, date_file_count, keywords, output_path):
    """
    保存结果为CSV：
    - 每个日期先输出「新闻数量」行（日期, 新闻数量, 当日文件数）
    - 再输出该日期下所有关键词行（每个关键词仅一行）
    """
    # 按日期排序，保证结果有序
    sorted_dates = sorted(date_kw_total.keys())

    # 写入CSV（utf-8-sig解决Excel中文乱码）
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['日期', '关键词', '当天出现总次数'])

        # 遍历每个日期
        for date in sorted_dates:
            # 第一步：写入该日期的「新闻数量」行
            news_count = date_file_count.get(date, 0)
            writer.writerow([date, '新闻数量', news_count])

            # 第二步：写入该日期下所有关键词行（每个关键词仅一行）
            for kw in keywords:
                total_count = date_kw_total[date][kw]
                writer.writerow([date, kw, total_count])

    print(f"\n✅ 结果已保存至：{os.path.abspath(output_path)}")


if __name__ == "__main__":
    # ====================== 固定配置（无需修改）======================
    # 输入文件夹路径
    INPUT_FOLDER = r'E:\code\python\energy_internet\2025\临时文件\人民网新闻原文-能源互联网'
    # 输出CSV路径（V3版本）
    OUTPUT_CSV = r'E:\code\python\energy_internet\2025\临时文件\V8人民网新闻原文-能源互联网关键词频率统计.csv'
    # 关键词列表（无"新闻数量"，单独处理）
    KEYWORDS = [
        '多能互补', '碳中和', '碳达峰', '柔性输电', '综合能源', '氢能',
        '电动汽车', '分布式交易', '微网', '新型电力系统', '储能', 'CCHP',
        '燃料电池', '能源物联网', '能源大数据', '电力交易', '能效', '节能',
        '区块链', '虚拟电厂', '能量路由器', '多能流', '需求侧', '抽水蓄能',
        '电化学储能'
    ]
    # 文件编码（优先用utf-8，乱码则改为gbk）
    FILE_ENCODING = 'utf-8'
    # 校验配置：20250119 电动汽车 预期值3
    VALIDATE_DATE = '20250119'
    VALIDATE_KEYWORD = '电动汽车'
    VALIDATE_EXPECTED = 3
    # ======================================================================

    # 1. 批量处理文件，获取日期-关键词总次数 + 日期-新闻数量
    date_kw_total, date_file_count = batch_process_files(INPUT_FOLDER, KEYWORDS, FILE_ENCODING)

    # 2. 校验20250119电动汽车的统计结果
    if date_kw_total:
        validate_specific_data(date_kw_total, VALIDATE_DATE, VALIDATE_KEYWORD, VALIDATE_EXPECTED)
    else:
        print("❌ 无统计数据，跳过校验")

    # 3. 保存为指定格式的CSV（含新闻数量行）
    if date_kw_total:
        save_to_csv(date_kw_total, date_file_count, KEYWORDS, OUTPUT_CSV)
    else:
        print("❌ 未统计到任何有效关键词记录，未生成CSV")

    # 4. 打印20250119全量数据（便于核对）
    if VALIDATE_DATE in date_kw_total:
        print(f"\n📋 {VALIDATE_DATE} 所有统计数据：")
        print(f"   新闻数量：{date_file_count.get(VALIDATE_DATE, 0)}")
        for kw, count in sorted(date_kw_total[VALIDATE_DATE].items()):
            print(f"   {kw}: {count} 次")