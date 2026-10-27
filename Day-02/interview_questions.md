# Day 2 Interview Questions: Messages, System Prompts, Parameters

Questions an interviewer might ask about what you built on Day 2: message roles, system prompts, temperature and tokens.
Answer in your own words. Say the short version first, then add detail if they ask.

---

## Section A: Message roles

### 1. What are the three message roles?
**Answer:**
- `system`: instructions for how the model should behave (tone, persona, rules, format).
- `user`: what the person asks.
- `assistant`: what the model replied earlier.

### 2. Why do you send `assistant` messages back to the model?
**Answer:** The model is **stateless**: it remembers nothing between API calls. To continue a conversation, I send the whole history again, including its own earlier replies as `assistant` messages. In my script, the model knew my name only because the earlier user message was in the list.

### 3. What is the downside of sending the whole history every time?
**Answer:** Every call gets bigger, so input tokens, cost and latency grow as the chat goes on. Eventually the history can exceed the model's **context window**. Common fixes are keeping only the last N turns, summarizing old turns, or retrieving only the relevant parts (RAG, covered in Phase 3).

### 4. Can you write a fake `assistant` message?
**Answer:** Yes. The model treats whatever is in the list as what was said. That's how few-shot examples work (Day 3): you write example user/assistant pairs to show the format you want.

---

## Section B: System prompts

### 5. What is a system prompt, and how is it different from a user prompt?
**Answer:** The system prompt sets lasting behavior for the whole conversation: who the model is, its tone, rules and output format. The user prompt is the specific request. Models follow the system prompt more strongly, so it's where rules like "answer only from the given context" belong.

### 6. What did you observe when you used 3 system prompts on the same question?
**Answer:** With the same question ("What is inflation?") and temperature 0, only the system prompt changed:
- "Explain to a 10-year-old" gave a simple answer with an everyday example (135 output tokens).
- "Economics professor" gave a formal definition with a formula, a cause and an effect (367 tokens).
- "One-line answers only" gave a single sentence (117 tokens).

The system prompt changed the length, style and cost more than anything else.

### 7. What makes a good system prompt?
**Answer:** A clear role, a specific task, explicit rules (length, format, what not to do), and the audience. "Maximum 3 sentences" works better than "be brief", because it can be checked.

### 8. What is a persona, and where is it useful?
**Answer:** A persona is a system prompt that gives the model a character, like teacher, lawyer or friend. It's useful for tutoring bots, customer support with a brand voice, and role-play training. In my persona playground, the lawyer focused on rights, risks and written evidence, while the friend gave the same advice casually.

### 9. Can a user override the system prompt?
**Answer:** Sometimes. That's **prompt injection** (for example "ignore your instructions and..."). System prompts help but aren't a security boundary. Real apps also validate outputs and limit what the model can actually do (covered on Day 24 for SQL).

---

## Section C: Parameters

### 10. What does temperature do?
**Answer:** It controls randomness when the model picks the next token. At 0 it almost always picks the most likely token, so answers repeat. Higher values (around 1) pick less likely tokens more often, so answers are more varied. In my test, temperature 0 gave "Serenity Steep Lounge" 3 times, and 1.0 gave 3 different names.

### 11. When would you use a low or a high temperature?
**Answer:**
- **Low (0 to 0.3):** facts, extraction, JSON output, SQL, RAG answers, evaluation. You want correct, repeatable results.
- **High (0.7 to 1):** brainstorming, names, creative writing, casual chat.

### 12. Does temperature 0 guarantee the same answer every time?
**Answer:** Nearly, but not exactly. Small numerical differences on the provider's hardware can still change the output occasionally. For strict repeatability you also save the output.

### 13. What is `max_tokens`, and what is `finish_reason`?
**Answer:** `max_tokens` caps the length of one reply. `finish_reason` tells you why the model stopped: `"stop"` means it finished naturally, and `"length"` means it hit `max_tokens` and the answer is cut off. Production code should check for `"length"`.

### 14. Name other common parameters.
**Answer:** `top_p` (another way to control randomness; usually change either it or temperature, not both), `stop` (strings that end generation), `seed` (for more repeatable outputs on some providers), and `stream` (receive tokens as they're generated, covered on Day 4).

---

## Section D: Tokens and cost

### 15. Why did a one-sentence answer use 117 output tokens?
**Answer:** `gpt-oss-120b` is a reasoning model. It generates hidden "thinking" tokens before the visible answer, and those count as output tokens. So output tokens are more than the words you can see. This matters for cost and for choosing `max_tokens`.

### 16. Why did the input tokens differ between personas when the question was the same?
**Answer:** The system prompt is part of the input. A longer system prompt means more input tokens on **every** call, so long system prompts cost more at scale.

### 17. What is a context window?
**Answer:** The maximum number of tokens (input plus output) the model can handle in one call. The system prompt, history, question and answer all have to fit inside it.

---

## Section E: The code

### 18. Walk me through `persona_playground.py`.
**Answer:** It defines a dictionary of personas (name to system prompt). It asks the user for one question, then loops over the personas. For each one it sends `[system persona, user question]` to the model and prints the answer with its token counts. It appends everything to `persona_replies.txt` with a timestamp, so earlier runs are kept.

### 19. Why open the file with `encoding="utf-8"` and mode `"a"`?
**Answer:** `utf-8` handles any character the model returns (curly quotes, non-breaking hyphens, Hindi text); Windows' default `cp1252` crashes on some of them. Mode `"a"` (append) adds to the file instead of overwriting it, so every comparison is kept.

### 20. What bug did you hit, and how did you fix it?
**Answer:** `UnicodeEncodeError: 'charmap' codec can't encode character ' '`. The model returned a special space character and Windows' console encoding couldn't print it. I fixed it with `sys.stdout.reconfigure(encoding="utf-8")` at the top of each script.

---

## Quick revision: one-line answers
- **system / user / assistant:** how to behave / the request / the model's past replies.
- **Stateless:** the model has no memory, so you send the history every call.
- **System prompt:** the strongest lever on style, length and cost.
- **temperature:** 0 = repeatable, about 1 = creative.
- **max_tokens + finish_reason:** the length limit; `"length"` means the reply was cut off.
- **Reasoning tokens:** hidden thinking that you still pay for.
- **Context window:** everything in one call has to fit.
