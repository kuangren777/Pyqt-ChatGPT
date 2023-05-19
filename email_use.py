import sqlite3
import smtplib
from email_use.mime.multipart import MIMEMultipart
from email_use.mime.text import MIMEText

# 连接到SQLite数据库
conn = sqlite3.connect('your_database.db')  # 替换为实际的数据库文件路径
cursor = conn.cursor()

# 执行查询语句
cursor.execute('SELECT * FROM your_table')  # 替换为实际的表名

# 获取查询结果
result = cursor.fetchall()

# 关闭数据库连接
cursor.close()
conn.close()

# 将查询结果转换为字符串格式
result_str = '\n'.join([str(row) for row in result])

# 配置电子邮件信息
sender_email = 'your_email@example.com'  # 替换为发件人邮箱
receiver_email = 'recipient_email@example.com'  # 替换为收件人邮箱
subject = 'SQLite Database Backup'
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
message.attach(MIMEText(result_str, 'plain'))

# 配置SMTP服务器信息
smtp_server = 'smtp.example.com'  # 替换为SMTP服务器地址
smtp_port = 587  # 替换为SMTP服务器端口号
smtp_username = 'your_username'  # 替换为SMTP账号用户名
smtp_password = 'your_password'  # 替换为SMTP账号密码

# 发送电子邮件
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
