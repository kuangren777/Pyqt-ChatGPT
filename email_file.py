import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_email_with_attachment(sender_email, receiver_email, subject, message, attachment_path, smtp_server, smtp_port,
                               smtp_username, smtp_password):
    # 配置电子邮件信息
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # 添加文本消息
    msg.attach(MIMEText(message, 'plain'))

    # 添加数据库文件附件
    with open(attachment_path, 'rb') as file:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(file.read())

    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f"attachment; filename=database.db")  # 设置附件名称

    msg.attach(attachment)

    # 配置SMTP服务器信息
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # 发送电子邮件
    server.send_message(msg)
    server.quit()


# 配置电子邮件和SMTP服务器信息
sender_email = 'your_email@example.com'  # 替换为发件人邮箱
receiver_email = 'recipient_email@example.com'  # 替换为收件人邮箱
subject = 'SQLite Database Backup'
message = 'Please find attached the SQLite database backup.'
attachment_path = 'path_to_database/database.db'  # 替换为实际的数据库文件路径
smtp_server = 'smtp.example.com'  # 替换为SMTP服务器地址
smtp_port = 587  # 替换为SMTP服务器端口号
smtp_username = 'your_username'  # 替换为SMTP账号用户名
smtp_password = 'your_password'  # 替换为SMTP账号密码

# 发送电子邮件
send_email_with_attachment(sender_email, receiver_email, subject, message, attachment_path, smtp_server, smtp_port,
                           smtp_username, smtp_password)
