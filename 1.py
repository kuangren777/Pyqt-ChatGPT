import openai

openai.api_key = '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'

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "user", "content": "请帮我写一个c#的程序，要从1的阶乘一直加到10的阶乘"},
    ]
)

print(response['choices'][0]['message']['content'])
