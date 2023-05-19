import re
import requests

session = requests.session()
url_set_key = "http://vipvip.icu/setsession.php"
# open_ai_key = "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"
open_ai_key = "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"
url_stream = "http://vipvip.icu/stream.php"

pattern = re.compile(r'"choices":\[{"delta":{"content":"(.*?)"},"index":')
flag = True
used = []
while True:
    ask_t = input()

    used_to_string = str(used).replace("\'", '\"')
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
        print("未连接成功")
        continue
    else:
        print("连接成功，等待生成……")
    res_stream = session.get(url=url_stream, data=data_stream)
    text_stream = res_stream.text
    matches = pattern.findall(text_stream)
    ans_t = """"""
    for match in matches:
        ans_t += match
    used.append([ask_t, ans_t])
    # print(used_to_string)
    if not ans_t:
        print("系统繁忙，请稍后重试！")
    ans_t = ans_t.replace("\\n", "\n")
    return ans_t