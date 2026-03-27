import os
import re
import csv


def extract_date_from_filename(filename):
    """从文件名提取前8位数字作为日期"""
    date_pattern = re.compile(r'^\d{8}')
    match = date_pattern.match(filename)
    return match.group() if match else ""


def count_keywords_in_single_file(file_path, keywords, encoding='utf-8'):
    """统计单个TXT文件中各关键词的出现次数"""
    keyword_count = {kw: 0 for kw in keywords}
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read().lower()  # 转小写实现不区分大小写统计

        for keyword in keywords:
            # 正则匹配完整词语，避免部分匹配（如"储能"不匹配"电化学储能"中的片段）
            pattern = re.compile(r'\b' + re.escape(keyword.lower()) + r'\b')
            keyword_count[keyword] = len(pattern.findall(content))
    except Exception as e:
        print(f"⚠️ 读取文件 {file_path} 出错: {str(e)}")
        # 出错时计数设为-1，便于识别异常
        keyword_count = {kw: -1 for kw in keywords}
    return keyword_count


def batch_process_files(folder_path, keywords, encoding='utf-8'):
    """批量处理所有TXT文件，按日期汇总关键词总次数"""
    # 存储日期→关键词→总次数的映射
    date_keyword_total = {}
    # 统计每个日期的文件数量（新闻数量）
    date_file_count = {}

    # 校验文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"❌ 错误：文件夹 {folder_path} 不存在！")
        return date_keyword_total, date_file_count

    # 筛选所有txt文件
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    print(f"📂 找到 {len(txt_files)} 个TXT文件，开始处理...")

    for filename in txt_files:
        # 提取日期
        date_str = extract_date_from_filename(filename)
        if not date_str:
            print(f"⚠️ 文件 {filename} 无有效日期，跳过")
            continue

        # 更新日期对应的新闻数量
        date_file_count[date_str] = date_file_count.get(date_str, 0) + 1

        # 统计当前文件的关键词次数
        file_path = os.path.join(folder_path, filename)
        file_kw_count = count_keywords_in_single_file(file_path, keywords, encoding)

        # 合并到日期总统计中
        if date_str not in date_keyword_total:
            date_keyword_total[date_str] = {kw: 0 for kw in keywords}

        for kw in keywords:
            if file_kw_count[kw] != -1:  # 跳过异常文件的计数
                date_keyword_total[date_str][kw] += file_kw_count[kw]

    return date_keyword_total, date_file_count


def save_to_csv(date_kw_total, date_file_count, keywords, output_path):
    """
    保存结果为CSV：每行格式 → 日期, 关键词, 当天该关键词总次数
    特别处理"新闻数量"关键词：值为当天的文件数
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
            # 先写入"新闻数量"这一行
            writer.writerow([date, '新闻数量', date_file_count.get(date, 0)])
            # 再写入该日期下所有关键词的统计行
            for kw in keywords:
                if kw != '新闻数量':  # 避免重复写入
                    writer.writerow([date, kw, date_kw_total[date][kw]])

    print(f"✅ 结果已保存至：{os.path.abspath(output_path)}")


if __name__ == "__main__":
    # ====================== 固定配置（无需修改）======================
    # 输入文件夹路径
    INPUT_FOLDER = r'E:\code\python\energy_internet\2025\临时文件\中新网新闻原文-新型电力系统'
    # 输出CSV路径
    OUTPUT_CSV = r'E:\code\python\energy_internet\2025\临时文件\V2中新网新闻原文-新型电力系统关键词频率统计.csv'
    # 关键词列表（包含新闻数量）
    KEYWORDS = [
        '新闻数量', '多能互补', '碳中和', '碳达峰', '柔性输电', '综合能源', '氢能',
        '电动汽车', '分布式交易', '微网', '新型电力系统', '储能', 'CCHP',
        '燃料电池', '能源物联网', '能源大数据', '电力交易', '能效', '节能',
        '区块链', '虚拟电厂', '能量路由器', '多能流', '需求侧', '抽水蓄能',
        '电化学储能'
    ]
    # 文件编码（乱码时改为gbk/gb2312）
    FILE_ENCODING = 'utf-8'
    # ======================================================================

    # 1. 批量处理文件，按日期汇总关键词次数
    date_kw_total, date_file_count = batch_process_files(INPUT_FOLDER, KEYWORDS, FILE_ENCODING)

    # 2. 保存为指定格式的CSV
    if date_kw_total:
        save_to_csv(date_kw_total, date_file_count, KEYWORDS, OUTPUT_CSV)
    else:
        print("❌ 未统计到任何有效数据！")

    # 3. 打印简要统计结果
    print("\n📊 统计完成！各日期数据量：")
    for date in sorted(date_kw_total.keys()):
        print(f"日期 {date}：{date_file_count[date]} 篇新闻")