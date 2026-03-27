import os
import re
from collections import Counter
import csv


def extract_date_from_filename(filename):
    """
    从文件名中提取前8位作为日期
    Args:
        filename: 文件名（如 20250323_新闻.txt）
    Returns:
        提取的日期字符串（如 20250323），提取失败返回空字符串
    """
    # 匹配前8位数字
    date_pattern = re.compile(r'^\d{8}')
    match = date_pattern.match(filename)
    if match:
        return match.group()
    return ""


def count_keywords_in_txt(file_path, keywords, encoding='utf-8'):
    """
    统计单个TXT文件中指定关键词的出现次数
    Args:
        file_path: 文件完整路径
        keywords: 关键词列表
        encoding: 文件编码
    Returns:
        字典，键为关键词，值为出现次数
    """
    keyword_count = {kw: 0 for kw in keywords}

    try:
        with open(file_path, 'r', encoding=encoding) as f:
            # 读取文件内容并转为小写（不区分大小写统计）
            content = f.read().lower()

        # 统计每个关键词的出现次数（匹配完整词语）
        for keyword in keywords:
            # 转小写并转义特殊字符，避免正则匹配出错
            keyword_lower = keyword.lower()
            pattern = re.compile(r'\b' + re.escape(keyword_lower) + r'\b')
            matches = pattern.findall(content)
            keyword_count[keyword] = len(matches)

    except Exception as e:
        print(f"⚠️ 读取文件 {file_path} 出错: {str(e)}")
        # 出错时所有关键词计数设为-1，便于后续识别异常文件
        keyword_count = {kw: -1 for kw in keywords}

    return keyword_count


def batch_process_txt_files(folder_path, keywords, encoding='utf-8'):
    """
    批量处理文件夹下所有TXT文件，统计关键词频率
    Args:
        folder_path: 文件夹路径
        keywords: 关键词列表
        encoding: 文件编码
    Returns:
        字典，键为日期，值为该日期下的关键词统计结果（合并同日期文件）
    """
    # 存储最终结果：{日期: {关键词: 总次数}}
    date_keyword_stats = {}
    # 统计每个日期的文件数量
    date_file_count = {}

    # 校验文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"❌ 错误：文件夹路径 {folder_path} 不存在！")
        return date_keyword_stats, date_file_count

    # 遍历文件夹下所有文件
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    print(f"📂 找到 {len(file_list)} 个TXT文件，开始处理...")

    for filename in file_list:
        # 提取日期
        date_str = extract_date_from_filename(filename)
        if not date_str:
            print(f"⚠️ 文件 {filename} 无法提取日期，跳过")
            continue

        # 更新日期对应的文件数量
        date_file_count[date_str] = date_file_count.get(date_str, 0) + 1

        # 拼接文件完整路径
        file_path = os.path.join(folder_path, filename)

        # 统计当前文件的关键词次数
        file_keyword_count = count_keywords_in_txt(file_path, keywords, encoding)

        # 合并到日期对应的总统计结果中
        if date_str not in date_keyword_stats:
            date_keyword_stats[date_str] = {kw: 0 for kw in keywords}

        for kw in keywords:
            # 跳过异常文件的计数（-1）
            if file_keyword_count[kw] != -1:
                date_keyword_stats[date_str][kw] += file_keyword_count[kw]

    return date_keyword_stats, date_file_count


def save_to_csv(result_data, file_count_data, keywords, output_path='关键词频率统计结果.csv'):
    """
    将统计结果保存为CSV表格
    Args:
        result_data: 日期-关键词统计字典
        file_count_data: 日期-文件数量字典
        keywords: 关键词列表
        output_path: 输出CSV路径
    """
    # 按日期排序
    sorted_dates = sorted(result_data.keys())

    # 写入CSV文件
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        # utf-8-sig 解决Excel打开中文乱码问题
        writer = csv.writer(f)

        # 写入表头：日期 + 新闻数量 + 关键词列表
        header = ['日期', '新闻数量'] + keywords
        writer.writerow(header)

        # 写入每行数据
        for date in sorted_dates:
            row = [
                date,  # 日期
                file_count_data.get(date, 0),  # 新闻数量
                *[result_data[date][kw] for kw in keywords]  # 各关键词次数
            ]
            writer.writerow(row)

    print(f"✅ 统计结果已保存至：{os.path.abspath(output_path)}")


if __name__ == "__main__":
    # ====================== 配置参数（无需修改其他部分）======================
    # 文件夹路径（使用r前缀避免转义问题）
    FOLDER_PATH = r'E:\code\python\energy_internet\2025\临时文件\中新网新闻原文-新型电力系统'
    # 关键词列表（包含你指定的所有关键词）
    KEYWORDS = [
        '多能互补', '碳中和', '碳达峰', '柔性输电', '综合能源', '氢能',
        '电动汽车', '分布式交易', '微网', '新型电力系统', '储能', 'CCHP',
        '燃料电池', '能源物联网', '能源大数据', '电力交易', '能效', '节能',
        '区块链', '虚拟电厂', '能量路由器', '多能流', '需求侧', '抽水蓄能',
        '电化学储能'
    ]
    # 文件编码（如果读取乱码，可改为gbk/gb2312）
    FILE_ENCODING = 'utf-8'
    # 输出CSV文件名
    OUTPUT_CSV_NAME = r'E:\code\python\energy_internet\2025\临时文件\中新网新闻原文-新型电力系统关键词频率统计.csv'
    # ======================================================================

    # 1. 批量处理文件，统计关键词频率
    date_keyword_stats, date_file_count = batch_process_txt_files(
        FOLDER_PATH, KEYWORDS, FILE_ENCODING
    )

    # 2. 保存结果到CSV表格
    if date_keyword_stats:
        save_to_csv(date_keyword_stats, date_file_count, KEYWORDS, OUTPUT_CSV_NAME)
    else:
        print("❌ 未统计到任何有效数据！")

    # 3. 打印简要结果
    print("\n📊 统计完成！简要结果：")
    for date in sorted(date_keyword_stats.keys()):
        print(f"日期 {date}：共 {date_file_count[date]} 篇新闻")