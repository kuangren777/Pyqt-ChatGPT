import re

pattern = r"(\d{2})-(\d{2})-(\d{4})"  # 匹配日期格式：dd-mm-yyyy
text = "Today's date is 17-05-2023."

# 使用捕获组提取匹配内容
match = re.search(pattern, text)
if match:
    # 获取所有捕获组的内容列表
    groups = match.groups()

    # 遍历捕获组列表并处理内容
    for group in groups:
        print("Group content:", group)
else:
    print("No match.")
