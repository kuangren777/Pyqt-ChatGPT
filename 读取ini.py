import configparser

# 创建 ConfigParser 对象
config = configparser.ConfigParser()

# 读取配置文件
config.read('config.ini')

# 获取配置值
api_key = config.get('API', 'api_key')


# 使用配置值
print(f'API Key: {api_key}')
