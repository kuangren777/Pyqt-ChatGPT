import tkinter as tk

def send_message(event=None):
    message = entry.get("1.0", tk.END).strip()
    if message:
        dialog.configure(state='normal')
        dialog.insert(tk.END, f'You: {message}\n')
        dialog.configure(state='disabled')
    entry.delete("1.0", tk.END)

root = tk.Tk()
root.title("Chat Interface")

# 创建对话框
dialog = tk.Text(root, state='disabled')
dialog.pack(fill=tk.BOTH, expand=True)

# 创建输入栏
entry = tk.Text(root, height=4)
entry.pack(fill=tk.X, padx=10, pady=10)

# 绑定 Ctrl+Enter 键盘事件
entry.bind("<Control-Return>", send_message)

# 创建发送按钮
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

root.mainloop()
