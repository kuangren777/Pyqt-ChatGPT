import sys
import tkinter as tk
import openai  # 0.27.0以上

openai.api_key = '自己去某宝或其他途径买api_key'


class ChatUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('ChatGPT')
        # 信息显示区域
        self.text_box = tk.Text(self.root, state=tk.DISABLED)
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # 输入框
        self.input_box = tk.Text(self.root, height=4)
        self.input_box.pack(padx=10, pady=10, fill=tk.X)
        # 创建一个发送消息的按钮
        self.send_button = tk.Button(self.root, text="发送", command=self.send_message)
        self.send_button.pack(padx=10, pady=5, side=tk.RIGHT)
        # 绑定 Ctrl+Enter 键盘事件
        self.input_box.bind("<Control-Return>", self.send_message)
        # 请求信息, 初始设置gpt扮演的身份，这里让其扮演程序员，可自行修改
        self.messages = [{"role": "system", "content": "你是一名程序员，可以替用户解决需求。"}]

    def start(self):
        self.root.mainloop()

    def send_message(self, event=None):
        # 获取输入框中的内容
        message = self.input_box.get("1.0", tk.END).strip()
        self.input_box.delete("1.0", tk.END)
        # 判断是否为结束符
        if message == 'z' or message == '结束':
            sys.exit()
        self.messages.append({"role": "user", "content": message})
        # 获取响应信息
        response = 'GPT:' + self.get_response() + '\n'
        # 拼接输入的消息
        message = '我: ' + message + '\n' + response
        # 在文本区域显示消息
        self.show_message(message)

    def get_response(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return completion.choices[0].message.content

    def show_message(self, message):
        # 在文本区域显示消息
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, message)
        self.text_box.config(state=tk.DISABLED)
        self.text_box.see(tk.END)  # 移动滚动条


if __name__ == '__main__':
    chat_ui = ChatUI()
    chat_ui.start()
