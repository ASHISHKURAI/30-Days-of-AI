from dotenv import load_dotenv
from groq import Groq

load_dotenv()                      # reads your .env file (searches parent folders too)
client = Groq()                    # finds GROQ_API_KEY by itself

reply = client.chat.completions.create(
    model="openai/gpt-oss-120b",      # check console.groq.com/docs/models for current names
    max_tokens=300,                   # maximum length of the answer
    messages=[
{"role": "user", "content": "Explain the rules of cricket in 3 simple lines."}
    ],
)

print(reply.choices[0].message.content)  # the answer text
print(reply.usage.prompt_tokens, reply.usage.completion_tokens)  # tokens in, tokens out
