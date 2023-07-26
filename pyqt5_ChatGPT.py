import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont
import openai
import threading
import json
import re
import requests
from datetime import datetime
import sqlite3
import configparser

openai.api_key = '自己去某宝或其他途径买api_key'


def get_key():
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config.get('API', 'api_key')


class ChatUI(QtWidgets.QMainWindow):
    new_info = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.chat_id = None
        self.get_chat_id()
        self.messages = """"""
        self.used = []
        self.open_ai_key = get_key()
        self.setWindowTitle('龚敏的神奇海螺_v1')
        self.new_info.connect(self.show_message)

        self.text_box = QtWidgets.QTextEdit()
        self.text_box.setReadOnly(True)

        self.input_box = QtWidgets.QTextEdit()
        self.input_box.setMaximumHeight(100)
        self.input_box.setPlaceholderText("输入消息")

        self.send_button = QtWidgets.QPushButton("发送")
        self.send_button.clicked.connect(self.send_message)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_box)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setGeometry(100, 100, 800, 600)
        self.create_shortcut()  # 创建快捷键
        self.chat_id_show_message = "当前聊天编号为:" + str(self.chat_id) + "\n"
        self.show_message(self.chat_id_show_message)

        self.host = None
        self.domain = None
        self.get_host()

    def get_host(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.host = config.get('SERVER', 'host')
        self.domain = config.get('SERVER', 'domain')

    def create_shortcut(self):
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_Return), self.input_box)
        shortcut.activated.connect(self.send_message)

    def send_message(self):
        self.messages = self.input_box.toPlainText().strip()
        self.input_box.clear()
        message = '\n' + '我： ' + self.messages + '\n'
        self.show_message(message)

        if self.messages == 'z' or self.messages == '结束':
            sys.exit()

        # self.messages.append({"role": "user", "content": message})

        threading.Thread(target=self.get_response_thread).start()

    def get_response_thread(self):
        response = self.get_response()
        # message = 'GPT:' + response + '\n'
        # self.show_message(message)

    def get_response_openai(self):
        completion = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return completion.choices[0].message["content"]

    def get_chat_id(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        chat_id_obj = cursor.execute("select max(chat_id) from gpt")
        self.chat_id = chat_id_obj.fetchall()[0][0] + 1

    def get_response(self):
        error = False
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        session = requests.session()
        url_set_key = f"http://{self.host}.{self.domain}/setsession.php"
        # open_ai_key = "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"

        url_stream = f"http://{self.host}.{self.domain}/stream.php"

        pattern = re.compile(r'"choices":\[{"delta":{"content":"(.*?)"},"index":')
        ask_t = self.messages

        used_to_string = str(self.used).replace("\'", '\"')
        print(used_to_string)
        head = {
            "Referer": f"http://{self.host}.{self.domain}/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.38"
        }

        data_set_session = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Length": "521",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": f"{self.host}.{self.domain}",
            "Origin": f"http://{self.host}.{self.domain}",
            "Referer": f"http://{self.host}.{self.domain}/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "message": ask_t,
            "context": used_to_string,
            "key": self.open_ai_key,
            "Proxy-Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest",
            "Dnt": "1",
        }

        data_stream = {
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip, deflate",
            "AcceptLanguage": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Dnt": "1",
            "Host": f"{self.host}.{self.domain}",
            "Proxy-Connection": "keep-alive",
            "Referer": f"http://{self.host}.{self.domain}/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }

        res_1 = session.post(url=url_set_key, data=data_set_session)
        response_data_1 = json.loads(res_1.content)
        success = response_data_1["success"]
        if not success:
            return "未连接成功\n"
        res_stream = session.get(url=url_stream, data=data_stream, stream=True)
        err_code = res_stream.headers['Set-Cookie']
        error_messages = {
            "invalid_api_key": "key不合法，请联系管理员",
            "context_length_exceeded": "问题和上下文长度超限，请重新提问",
            "rate_limit_reached": "同时访问用户过多，请稍后再试",
            "access_terminated": "违规使用，API-KEY被封禁",
            "no_api_key": "未提供API-KEY",
            "insufficient_quota": "API-KEY余额不足",
            "account_deactivated": "账户已禁用",
            "model_overloaded": "OpenAI模型超负荷，请重新发起请求"
        }
        # print(err_code)
        for error_message in error_messages:
            if error_message in err_code:
                self.show_message(error_messages[error_message])
                error = True
                continue
        if error:
            return "连接失败\n"
        self.show_message("连接成功\n")
        self.new_info.emit('GPT:')
        ans = ""
        ans_t = """"""
        for line in res_stream.iter_lines():
            if line:  # filter out keep-alive new lines
                text_stream = line.decode()
                matches = pattern.findall(text_stream)
                for match in matches:
                    ans = match

                    # print(ans_t)
                    ans = ans.replace("\\n", "\n")
                    ans = ans.replace('\\"', '\"')
                    ans = ans.replace("\\'", "\'")
                    ans = ans.replace("\\t", "\t")

                    ans_t += ans
                    self.new_info.emit(ans)
        # res_stream = session.get(url=url_stream, data=data_stream)
        # text_stream = res_stream.text
        # matches = pattern.findall(text_stream)
        # ans_t = """"""
        # for match in matches:
        #     ans_t += match
        self.used.append([ask_t, ans_t])
        # # print(used_to_string)
        # if not ans_t:
        #     return "系统繁忙，请稍后重试！"
        ans_t = ans_t.replace("\\n", "\n")
        threading.Thread(target=self.gpt_insert, args=(self.chat_id, ask_t, ans_t)).start()
        # self.gpt_insert(self.chat_id, ask_t, ans_t)
        # self.gpt_backup(self.chat_id, used_to_string)
        threading.Thread(target=self.gpt_backup, args=(self.chat_id, used_to_string)).start()
        # return ans_t
        session.close()

    def show_message(self, message):
        cursor = self.text_box.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(message)

        # Automatically scroll to the end of the text box
        scroll_bar = self.text_box.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

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
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('logo.png'))  # 替换为您的图标文件路径
    chat_ui = ChatUI()
    chat_ui.show()
    sys.exit(app.exec())
