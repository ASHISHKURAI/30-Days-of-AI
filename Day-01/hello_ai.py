# Day 1 real project: Hello AI
# Ask the model to explain a topic you actually care about in 3 simple lines.
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

topic = input("What topic should I explain? (e.g. GST, cricket rules): ")

reply = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    max_tokens=300,
    messages=[
        {"role": "user", "content": f"Explain {topic} in 3 simple lines."}
    ],
)

print()
print(reply.choices[0].message.content)
print(f"\nTokens used: {reply.usage.prompt_tokens} in, {reply.usage.completion_tokens} out")
