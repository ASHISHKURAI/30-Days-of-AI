# Day 2 learning script: roles and parameters
# Part 1 shows the three message roles (system, user, assistant).
# Part 2 asks the same question at temperature 0 and 1.0 to show the difference.
import sys
from dotenv import load_dotenv
from groq import Groq

sys.stdout.reconfigure(encoding="utf-8")  # lets Windows print any character the model sends
load_dotenv()                             # reads GROQ_API_KEY from the .env file in the main folder
client = Groq()                           # creates the connection to Groq using that key

MODEL = "openai/gpt-oss-120b"             # same model as Day 1; change it in one place here


# ---------- Part 1: the three roles ----------
# "system"    = instructions for HOW the model should behave (it never "says" this)
# "user"      = what you type
# "assistant" = what the model said earlier; we send it back so the model "remembers"
#
# The model has no memory between calls. Every call, we send the whole conversation again.
messages = [
    {"role": "system", "content": "You are a cricket coach. Keep every answer under 2 sentences."},
    {"role": "user", "content": "My name is Ashish. What is a yorker?"},
    {"role": "assistant", "content": "A yorker is a ball pitched right at the batter's feet, which makes it very hard to hit."},
    {"role": "user", "content": "What is my name, and how do I bowl that ball?"},
]

reply = client.chat.completions.create(
    model=MODEL,
    max_tokens=500,      # upper limit on the answer length (in tokens, roughly 3/4 of a word each)
    messages=messages,
)

print("=== Part 1: roles ===")
print(reply.choices[0].message.content)
# usage tells you how many tokens you paid for:
#   prompt_tokens     = everything you SENT (system + user + assistant messages)
#   completion_tokens = what the model WROTE back
print(f"Tokens: {reply.usage.prompt_tokens} in, {reply.usage.completion_tokens} out")
# finish_reason = "stop" means the model finished; "length" means max_tokens cut it off
print(f"Finish reason: {reply.choices[0].finish_reason}")


# ---------- Part 2: temperature ----------
# temperature controls randomness:
#   0   -> picks the most likely words, so the answer is nearly the same every time
#   1.0 -> takes more chances, so answers are more varied and creative
question = "Give me one creative name for a tea shop. Reply with only the name."

print("\n=== Part 2: temperature ===")
for temperature in [0, 1.0]:
    names = []
    for attempt in range(3):              # ask 3 times at each temperature
        reply = client.chat.completions.create(
            model=MODEL,
            max_tokens=500,
            temperature=temperature,
            messages=[{"role": "user", "content": question}],
        )
        names.append(reply.choices[0].message.content.strip())
    print(f"temperature={temperature}: {names}")

print("\nNotice: temperature 0 repeats itself, temperature 1.0 gives different names.")
