import sqlite3
from datetime import datetime

# 连接到数据库文件
conn = sqlite3.connect('database.db')

# 创建一个游标对象
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE gpt (
        id INTEGER PRIMARY KEY,
        chat_id INTEGER,
        ask TEXT,
        ans TEXT,
        date DATE,
        use_time TIME
    )
''')

cursor.execute('''
    CREATE TABLE gpt_backup (
        id INTEGER PRIMARY KEY,
        chat_id INTEGER,
        chats BLOB
    )
''')

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
''', (1, "1", "1", date_str, time_str))

cursor.execute('''
    INSERT INTO gpt_backup (chat_id, chats)
    VALUES (?, ?)
''', (1, "1"))

# 提交更改并关闭连接
conn.commit()
conn.close()
