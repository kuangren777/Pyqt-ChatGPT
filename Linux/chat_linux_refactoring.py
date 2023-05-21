import requests
import re
import json
import sqlite3
from datetime import datetime
import os
import configparser


# 根据操作系统不同执行相应的命令
def clear_screen():
    if os.name == 'nt':  # Windows
        _ = os.system('cls')
    else:  # Linux/MacOS
        _ = os.system('clear')


def get_connection_and_cursor():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    return conn, cursor


def read_configuration():
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config


def get_chat_id(cursor):
    chat_id_obj = cursor.execute("select max(chat_id) from gpt")
    chat_id = chat_id_obj.fetchall()[0][0] + 1
    return chat_id


def insert_data(cursor, conn, chat_id, ask, ans):
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


def backup_data(cursor, conn, chat_id, used):
    cursor.execute('''
            INSERT INTO gpt_backup (chat_id, chats)
            VALUES (?, ?)
        ''', (chat_id, used)
                   )
    # 提交更改并关闭连接
    conn.commit()


def process_request(session, ask_t, used_to_string, open_ai_key):
    url_set_key = "http://vipvip.icu/setsession.php"
    url_stream = "http://vipvip.icu/stream.php"

    pattern = re.compile(r'"choices":\[{"delta":{"content":"(.*?)"},"index":')

    head = {
        "Referer": "http://vipvip.icu/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.38"
    }

    data_set_session = {
        "message": ask_t,
        "context": used_to_string,
        "key": open_ai_key,
    }

    res_1 = session.post(url=url_set_key, data=data_set_session)
    response_data_1 = json.loads(res_1.content)

    return response_data_1


def close_cursor_and_connection(cursor, conn):
    cursor.close()
    conn.close()
    print("已退出数据库，同学再见！")


def main():
    clear_screen()

    conn, cursor = get_connection_and_cursor()
    config = read_configuration()

    open_ai_key = config.get('API', 'api_key')

    chat_id = get_chat_id(cursor)
    print("当前对话编号：", chat_id)

    try:
        print("欢迎使用图书馆专属对话系统，感谢ai.com提供的技术支持，请直接输入：")

        session = requests.session()
        url_stream = "http://vipvip.icu/stream.php"
        used = []
        while True:
            ask_t = input()

            used_to_string = str(used).replace("\'", '\"')

            response_data_1 = process_request(session, ask_t, used_to_string, open_ai_key)

            success = response_data_1["success"]
            if not success:
                print("未连接成功")
                continue
            else:
                print("连接成功，等待生成……")

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

            ans_t, error = process_stream(session, ask_t, used, data_stream, url_stream)
            if error:
                continue

            if not ans_t:
                print("系统繁忙，请稍后重试！")
            else:
                print(ans_t)
                insert_data(cursor, conn, chat_id, ask_t, ans_t)
                backup_data(cursor, conn, chat_id, used_to_string)

    except KeyboardInterrupt:
        print("检测到程序退出! 正在退出数据库……")

    finally:
        close_cursor_and_connection(cursor, conn)


def handle_error(error_messages, err_code):
    for error_message in error_messages:
        if error_message in err_code:
            print(error_messages[error_message])
            return True
    return False


def process_stream(session, ask_t, used, data_stream, url_stream):
    res_stream = session.get(url=url_stream, data=data_stream)
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

    error = handle_error(error_messages, err_code)
    if error:
        return None, True

    pattern = re.compile(r'"choices":\[{"delta":{"content":"(.*?)"},"index":')
    text_stream = res_stream.text
    matches = pattern.findall(text_stream)
    ans_t = """"""
    for match in matches:
        ans_t += match
    used.append([ask_t, ans_t])
    ans_t = ans_t.replace("\\n", "\n")

    return ans_t, False


if __name__ == "__main__":
    main()
