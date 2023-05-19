import os
import openai

api_key = "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"


openai.api_key = "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"

model_engine = "gpt-3.5-turbo"

prompt = "怎么在python上使用chat gpt"

completions = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
)

message = completions['choices'][0]['message']['content']
print(message)
