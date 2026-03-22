import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
from datetime import datetime


def convert_ms_to_datetime(ms_timestamp):
    """毫秒时间戳转指定格式字符串"""
    try:
        if not ms_timestamp:
            return ""
        # 确保是整数类型
        ms_int = int(ms_timestamp)
        dt = datetime.fromtimestamp(ms_int / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise Exception(f"时间戳格式错误：{ms_timestamp}（需为数字）")
    except Exception as e:
        raise Exception(f"时间转换失败：{str(e)}")


def json_to_csv_and_copy():
    """核心逻辑：解析JSON→生成CSV（无表头）→展示+复制到剪贴板"""
    try:
        # 1. 清空之前的输出
        output_text.delete("1.0", tk.END)

        # 2. 获取并校验输入
        json_text = input_text.get("1.0", tk.END).strip()
        if not json_text:
            messagebox.showerror("输入错误", "请先输入有效的JSON数据！")
            return

        # 3. 解析JSON
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON解析错误", f"JSON格式不合法：\n{e}")
            return

        # 4. 提取records数组
        records = data.get("data", {}).get("records", [])
        if not isinstance(records, list):
            messagebox.showerror("数据结构错误", "未找到有效格式：需包含 data -> records 数组！")
            return
        if len(records) == 0:
            messagebox.showwarning("数据为空", "records数组中无数据！")
            return

        # 5. 生成CSV内容（移除表头）
        csv_lines = []  # 不再添加表头行
        for idx, record in enumerate(records):
            try:
                display_time = record.get("displayTime", "")
                title = record.get("title", "").replace(",", "，")  # 替换逗号避免列错位
                url = record.get("url", "").replace(",", "，")
                time_str = convert_ms_to_datetime(display_time)
                csv_lines.append(f"{time_str},{title},{url}")
            except Exception as e:
                messagebox.showerror("单条数据处理错误", f"第{idx + 1}条数据异常：\n{e}")
                return

        # 6. 展示CSV内容
        csv_content = "\n".join(csv_lines)
        output_text.insert("1.0", csv_content)

        # 7. 复制到剪贴板
        root.clipboard_clear()
        root.clipboard_append(csv_content)

        # 8. 反馈结果
        messagebox.showinfo("操作成功", f"已成功转换{len(records)}条数据！\nCSV内容已复制到剪贴板（无表头）。")

    # 捕获所有未预期的异常
    except Exception as e:
        messagebox.showerror("系统错误", f"程序运行异常：\n{str(e)}")


# ========== GUI界面构建 ==========
root = tk.Tk()
root.title("JSON转CSV工具（无表头+结果预览）")
root.geometry("850x650")  # 优化窗口大小
root.resizable(False, False)  # 固定窗口尺寸

# 输入区域
input_label = tk.Label(root, text="请粘贴完整JSON数据：", font=("微软雅黑", 10))
input_label.pack(pady=(15, 5), anchor="w", padx=20)

input_text = scrolledtext.ScrolledText(
    root, width=95, height=12, font=("微软雅黑", 9), wrap=tk.WORD
)
input_text.pack(padx=20, fill="x")

# 核心按钮
convert_btn = tk.Button(
    root, text="转换并复制", command=json_to_csv_and_copy,
    font=("微软雅黑", 11), bg="#2196F3", fg="white",
    width=20, height=2, relief=tk.RAISED
)
convert_btn.pack(pady=10)

# 输出预览区域
output_label = tk.Label(root, text="CSV转换结果预览（无表头）：", font=("微软雅黑", 10))
output_label.pack(pady=(5, 5), anchor="w", padx=20)

output_text = scrolledtext.ScrolledText(
    root, width=95, height=15, font=("微软雅黑", 9), wrap=tk.WORD
)
output_text.pack(padx=20, fill="x")

# 启动主循环
root.mainloop()