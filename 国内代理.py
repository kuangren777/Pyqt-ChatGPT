import requests

# 123.144.63.19:16965
proxies = {
    "http": "http://183.221.242.107:8443",
}

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
}

r1 = requests.get("https://api-0-openai-com.mcwqzs.cn/", proxies=proxies, verify=False)
# r1 = requests.get("https://api-0-openai-com.mcwqzs.cn/", verify=False)
# r1.encoding = 'utf-8'
print(r1.text)