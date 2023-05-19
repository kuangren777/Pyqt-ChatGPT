from PyQt5 import QtCore, QtWidgets


class ChatWidget(QtWidgets.QWidget):
    new_info = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.text_edit = QtWidgets.QTextEdit()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text_edit)

        self.new_info.connect(self.update_chat)

    def update_chat(self, info):
        current_text = self.text_edit.toPlainText()
        if current_text:
            new_text = current_text + " " + info
        else:
            new_text = info
        self.text_edit.setPlainText(new_text)


# 示例用法
chat_widget = ChatWidget()
chat_widget.show()

# 发出信号
chat_widget.new_info.emit("Hello")
chat_widget.new_info.emit("World")
