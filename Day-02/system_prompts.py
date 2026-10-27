# Day 2 build: compare 3 system prompts
# Asks the SAME question under 3 different system prompts and saves the answers
# side by side in system_prompt_comparison.md, so you can see how much the
# system prompt changes the reply.
import sys
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

sys.stdout.reconfigure(encoding="utf-8")  # lets Windows print any character the model sends
load_dotenv()
client = Groq()

MODEL = "openai/gpt-oss-120b"
QUESTION = "What is inflation?"           # change this to any question you like

# Each system prompt gives the model a different job. The question stays the same.
SYSTEM_PROMPTS = {
    "Explain to a 10-year-old": "You explain things to a 10-year-old. Use simple words and one everyday example. Maximum 3 sentences.",
    "Economics professor": "You are an economics professor. Give a precise, formal definition and mention one cause and one effect.",
    "One-line answers only": "Answer in exactly one short sentence. No extra words.",
}

# The output file is saved next to this script, whichever folder you run it from
output_file = Path(__file__).parent / "system_prompt_comparison.md"

lines = [f"# System prompt comparison\n\n**Question:** {QUESTION}\n\n**Model:** {MODEL}\n"]

for label, system_prompt in SYSTEM_PROMPTS.items():
    reply = client.chat.completions.create(
        model=MODEL,
        max_tokens=800,
        temperature=0,                    # 0 keeps answers steady, so only the system prompt changes them
        messages=[
            {"role": "system", "content": system_prompt},   # HOW to answer
            {"role": "user", "content": QUESTION},          # WHAT to answer
        ],
    )
    answer = reply.choices[0].message.content.strip()
    tokens_in = reply.usage.prompt_tokens
    tokens_out = reply.usage.completion_tokens

    print(f"--- {label} ---\n{answer}\n(tokens: {tokens_in} in, {tokens_out} out)\n")

    # Build the markdown section for this system prompt
    lines.append(f"\n## {label}\n")
    lines.append(f"**System prompt:** {system_prompt}\n")
    lines.append(f"**Tokens:** {tokens_in} in, {tokens_out} out\n")
    lines.append(f"\n{answer}\n")

# Leave space for your own observations at the end
lines.append("\n## My notes\n\n- Which answer was most useful, and why?\n- Which one used the most tokens?\n")

# encoding="utf-8" so special characters save correctly on Windows
output_file.write_text("".join(lines), encoding="utf-8")
print(f"Saved to {output_file}")
