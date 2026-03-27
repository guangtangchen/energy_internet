import os
import re
from collections import Counter


def count_word_frequency_in_txt(folder_path, target_words, encoding='utf-8'):
    """
    统计指定文件夹下所有txt文件中目标词语的出现频率

    Args:
        folder_path: 文件夹路径（绝对路径/相对路径）
        target_words: 要统计的目标词语列表（如 ['数据', '分析', 'Python']）
        encoding: 文件编码格式，默认utf-8，可根据实际情况改为gbk等

    Returns:
        字典，键为文件名，值为该文件中各词语的频率统计
    """
    # 存储最终结果：{文件名: {词语: 次数}}
    result = {}

    # 校验文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹路径 {folder_path} 不存在！")
        return result

    # 遍历文件夹下所有文件
    for file_name in os.listdir(folder_path):
        # 只处理txt文件
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            print(f"正在处理文件：{file_path}")

            try:
                # 读取文件内容（处理大文件时建议按行读取，这里简化为一次性读取）
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read().lower()  # 转小写，实现不区分大小写统计

                # 初始化当前文件的统计结果
                word_count = {word: 0 for word in target_words}

                # 统计每个目标词语的出现次数（正则匹配完整词语，避免部分匹配）
                for word in target_words:
                    # 使用正则确保匹配完整词语（避免"数据分析"匹配到"数据"的问题）
                    pattern = re.compile(r'\b' + re.escape(word.lower()) + r'\b')
                    matches = pattern.findall(content)
                    word_count[word] = len(matches)

                # 将当前文件结果加入总结果
                result[file_name] = word_count

            except Exception as e:
                print(f"处理文件 {file_name} 时出错：{str(e)}")
                result[file_name] = f"读取失败：{str(e)}"

    return result


def print_result(result):
    """格式化打印统计结果"""
    print("\n===== 词语频率统计结果 =====")
    for file_name, count_dict in result.items():
        print(f"\n【{file_name}】")
        if isinstance(count_dict, dict):
            for word, count in count_dict.items():
                print(f"  {word}: {count} 次")
        else:
            print(f"  {count_dict}")


if __name__ == "__main__":
    # -------------------------- 配置参数 --------------------------
    # 替换为你的文件夹路径（绝对路径示例：r'C:\data\txt_files'；相对路径：'./txt_files'）
    FOLDER_PATH = r'E:\code\python\energy_internet\2025\临时文件\中新网新闻原文-新型电力系统'
    # 替换为你要统计的固定词语列表
    TARGET_WORDS = ['新闻数量', '多能互补']
    # 文件编码（如果文件是GBK编码，改为 'gbk'）
    FILE_ENCODING = 'utf-8'
    # -------------------------------------------------------------

    # 执行统计
    frequency_result = count_word_frequency_in_txt(FOLDER_PATH, TARGET_WORDS, FILE_ENCODING)

    # 打印结果
    print_result(frequency_result)

    # （可选）将结果保存为csv文件
    # import csv
    # with open('word_frequency_result.csv', 'w', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     # 写入表头
    #     writer.writerow(['文件名'] + TARGET_WORDS)
    #     # 写入数据
    #     for file_name, count_dict in frequency_result.items():
    #         if isinstance(count_dict, dict):
    #             row = [file_name] + [count_dict[word] for word in TARGET_WORDS]
    #         else:
    #             row = [file_name] + ['读取失败'] * len(TARGET_WORDS)
    #         writer.writerow(row)
    # print("\n结果已保存到 word_frequency_result.csv")