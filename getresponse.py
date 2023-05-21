import requests
import json

# 设置反向代理的地址和端口
proxy_address = 'api-0-openai-com.mcwqzs.cn'
proxy_port = 80

# 创建会话对象并设置代理
session = requests.Session()
session.proxies = {
    'http': f'http://{proxy_address}:{proxy_port}',
    'https': f'http://{proxy_address}:{proxy_port}'
}

# 设置请求头
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'  # 替换为你的 API 密钥或访问令牌
}

# 设置有效载荷数据
payload = {
    'prompt': '你是谁',
    'max_tokens': 50  # 生成的响应的最大标记数
}

# 发送 POST 请求
response = session.post(
    'https://api.openai.com/v1/engines/davinci-codex/completions',
    headers=headers,
    data=json.dumps(payload)
)

# 解析和处理响应
if response.status_code == 200:
    data = response.json()
    generated_text = data['choices'][0]['text']
    print(generated_text)
else:
    print('请求失败:', response.text)
