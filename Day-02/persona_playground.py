# Day 2 real project: Persona playground
# You type ONE question; the model answers it as a teacher, a lawyer and a friend.
# All three replies are saved in persona_replies.txt so you can compare them.
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

sys.stdout.reconfigure(encoding="utf-8")  # lets Windows print any character the model sends
load_dotenv()
client = Groq()

MODEL = "openai/gpt-oss-120b"

# A persona is just a system prompt. Add your own persona here to try it.
PERSONAS = {
    "Teacher": "You are a patient school teacher. Explain step by step in simple language. Keep it under 120 words.",
    "Lawyer": "You are a careful lawyer. Point out rights, risks and what to put in writing. Keep it under 120 words.",
    "Friend": "You are a casual, supportive friend. Talk informally and give honest, practical advice. Keep it under 120 words.",
}


def ask_persona(system_prompt, question):
    """Send one question with one persona and return (answer, tokens_in, tokens_out)."""
    reply = client.chat.completions.create(
        model=MODEL,
        max_tokens=800,
        temperature=0.7,                  # a little variety so personas sound natural
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return (
        reply.choices[0].message.content.strip(),
        reply.usage.prompt_tokens,
        reply.usage.completion_tokens,
    )


question = input("Ask one question (e.g. 'My landlord won't return my deposit. What should I do?'): ").strip()
if not question:                          # nothing typed: stop instead of sending an empty question
    print("No question given. Run the script again and type a question.")
    sys.exit()

output_file = Path(__file__).parent / "persona_replies.txt"

# "a" = append mode, so every run is ADDED to the file instead of replacing it
with open(output_file, "a", encoding="utf-8") as f:
    f.write(f"\n{'=' * 60}\n")
    f.write(f"{datetime.now():%Y-%m-%d %H:%M}  |  Question: {question}\n")
    f.write(f"{'=' * 60}\n")

    for name, system_prompt in PERSONAS.items():
        answer, tokens_in, tokens_out = ask_persona(system_prompt, question)
        block = f"\n[{name}]  (tokens: {tokens_in} in, {tokens_out} out)\n{answer}\n"
        print(block)
        f.write(block)

print(f"Saved all three replies to {output_file}")
