import json
import sys
import threading
import tkinter as tk
from tkinter import ttk
import re
import requests
from ttkthemes import ThemedTk
from datetime import datetime
import sqlite3
import openai  # 0.27.0以上

openai.api_key = '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'

class ChatUI:
    def __init__(self):
        # self.conn = sqlite3.connect('database.db')
        # self.cursor = self.conn.cursor()
        self.chat_id = None
        self.get_chat_id()
        self.messages = """"""
        self.used = []
        self.root = ThemedTk(theme="clearlooks")  # 更改主题为"clearlooks"
        self.root.title('龚敏的傻子助手Chatgpt')
        # 信息显示区域
        self.text_box = tk.Text(self.root, state=tk.DISABLED)
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # 输入框
        self.input_box = tk.Text(self.root, height=4)
        self.input_box.pack(padx=10, pady=10, fill=tk.X)
        # 创建一个发送消息的按钮
        self.send_button = ttk.Button(self.root, text="发送", command=self.send_message_thread)  # 绑定到新的线程函数
        self.send_button.pack(padx=10, pady=5, side=tk.RIGHT)
        # 绑定 Ctrl+Enter 键盘事件
        self.input_box.bind("<Control-Return>", self.send_message_thread)  # 绑定到新的线程函数
        # 请求信息, 初始设置gpt扮演的身份，这里让其扮演程序员，可自行修改
        # self.messages = [{"role": "system", "content": "你是一名程序员，可以替用户解决需求。"}]
        self.chat_id_show_message = "当前聊天编号为:" + str(self.chat_id) + "\n"
        self.show_message(self.chat_id_show_message)

    def get_chat_id(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        chat_id_obj = cursor.execute("select max(chat_id) from gpt")
        self.chat_id = chat_id_obj.fetchall()[0][0] + 1

    def start(self):
        # 创建并启动线程
        # thread = threading.Thread(target=self.thread_function)
        # thread.start()
        self.root.mainloop()

    def send_message_thread(self, event=None):
        # 使用线程来发送消息，防止UI阻塞
        threading.Thread(target=self.send_message, args=(event,)).start()

    def send_message(self, event=None):
        # 获取输入框中的内容
        self.messages = self.input_box.get("1.0", tk.END).strip()
        self.input_box.delete("1.0", tk.END)
        # 判断是否为结束符
        if self.messages == 'z' or self.messages == '结束':
            sys.exit()
        message = 'Me: ' + self.messages + '\n'
        self.show_message(message)
        # self.messages.append({"role": "user", "content": message})
        # 获取响应信息
        response = 'GPT:' + self.get_response() + '\n\n\n'
        # 在文本区域显示消息
        self.show_message(response)

    def get_response_openai(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return completion.choices[0].message.content

    def get_response(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        session = requests.session()
        url_set_key = "http://vipvip.icu/setsession.php"
        # open_ai_key = "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"
        open_ai_key = "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"
        url_stream = "http://vipvip.icu/stream.php"

        pattern = re.compile(r'"choices":\[{"delta":{"content":"(.*?)"},"index":')
        ask_t = self.messages

        used_to_string = str(self.used).replace("\'", '\"')
        head = {
            "Referer": "http://vipvip.icu/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.38"
        }

        data_set_session = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Length": "521",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "PHPSESSID=gkcftudq16e9v52uuf6gata73q",
            "Host": "vipvip.icu",
            "Origin": "http://vipvip.icu",
            "Referer": "http://vipvip.icu/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "message": ask_t,
            "context": used_to_string,
            "key": open_ai_key,
            "Proxy-Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest",
            "Dnt": "1",
        }

        data_stream = {
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip, deflate",
            "AcceptLanguage": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Cookie": "PHPSESSID=gkcftudq16e9v52uuf6gata73q",
            "Dnt": "1",
            "Host": "vipvip.icu",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://vipvip.icu/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }

        res_1 = session.post(url=url_set_key, data=data_set_session)
        response_data_1 = json.loads(res_1.content)
        success = response_data_1["success"]
        if not success:
            return "未连接成功"
        self.show_message("连接成功\n")
        res_stream = session.get(url=url_stream, data=data_stream)
        text_stream = res_stream.text
        matches = pattern.findall(text_stream)
        ans_t = """"""
        for match in matches:
            ans_t += match
        self.used.append([ask_t, ans_t])
        # print(used_to_string)
        if not ans_t:
            return "系统繁忙，请稍后重试！"
        ans_t = ans_t.replace("\\n", "\n")
        threading.Thread(target=self.gpt_insert, args=(self.chat_id, ask_t, ans_t)).start()
        # self.gpt_insert(self.chat_id, ask_t, ans_t)
        # self.gpt_backup(self.chat_id, used_to_string)
        threading.Thread(target=self.gpt_backup, args=(self.chat_id, used_to_string)).start()
        return ans_t

    def show_message(self, message):
        # 在文本区域显示消息
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, message)
        self.text_box.config(state=tk.DISABLED)
        self.text_box.see(tk.END)  # 移动滚动条

    def gpt_insert(self, chat_id, ask, ans):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # 生成当前日期和时间
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        # 将日期和时间对象转换为字符串
        date_str = current_date.strftime('%Y-%m-%d')
        time_str = current_time.strftime('%H:%M:%S')

        # 插入数据
        cursor.execute('''
            INSERT INTO gpt (chat_id, ask, ans, date, use_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, ask, ans, date_str, time_str)
                       )
        # 提交更改并关闭连接
        conn.commit()
        cursor.close()
        conn.close()

    def gpt_backup(self, chat_id, used):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO gpt_backup (chat_id, chats)
                VALUES (?, ?)
            ''', (chat_id, used)
                       )
        # 提交更改并关闭连接
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    chat_ui = ChatUI()
    chat_ui.start()
