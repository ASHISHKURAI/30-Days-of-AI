# Day 2: basic questions and cross-questions

Each topic starts with a **basic question**. The **cross-questions** under it are the follow-ups an interviewer asks to check that you really understand it. Answer out loud before you read the answer.

---

## 1. Message roles

**Basic: What are the three message roles?**
`system` says how to behave, `user` is what the person asks, and `assistant` is what the model said earlier.

**Cross-questions:**
- **Why send `assistant` messages back at all?** The model has no memory. Its earlier replies are part of the conversation only if you send them again.
- **Can you write a fake `assistant` message?** Yes. The model treats it as something it said. Day 3 uses this for few-shot examples.
- **What happens if you remove the `assistant` message from the yorker example?** The model loses its earlier answer, though it can still use general knowledge to explain a yorker.
- **Does the order of messages matter?** Yes. The model reads them as a timeline, and the last `user` message is the one it answers.

---

## 2. No memory

**Basic: Does the model remember earlier calls?**
No. Every call is independent. "Memory" is just the messages list you send again each time.

**Cross-questions:**
- **How did the model know your name in Part 1?** The earlier message "My name is Ashish" was sent again in the same call.
- **What is the downside of resending the whole history?** Input tokens grow every turn, so each call costs more, gets slower and eventually hits the context window.
- **How would you handle a very long chat?** Keep only the last few turns, or summarise old turns into one short message.

---

## 3. Context window

**Basic: What is a context window?**
The most tokens a model can handle in one call: your input plus its output.

**Cross-questions:**
- **What happens when the chat exceeds it?** The API returns an error, or you must drop or summarise old messages first.
- **Does a bigger context window mean better answers?** Not always. Important details can get lost in very long inputs, and every extra token costs money.

---

## 4. System prompt

**Basic: What is a system prompt?**
Instructions on how the model should answer: role, tone, rules and length. The user prompt says what to answer.

**Cross-questions:**
- **What did your 3-prompt comparison show?** The same question gave 135, 402 and 117 output tokens. The system prompt changed length, tone, structure and cost.
- **What makes a good system prompt?** A clear role, specific rules, the output length or format, and what to do in edge cases.
- **Why did input tokens differ (101, 98, 89) when the question was the same?** The system prompts had different lengths, and they count as input.
- **Can a user override the system prompt?** They can try ("ignore your instructions…"). This is prompt injection. The system prompt carries more weight, but it is not a guarantee, so real apps add checks in code.

---

## 5. Persona

**Basic: What is a persona?**
A system prompt that gives the model a character, like Teacher, Lawyer or Friend.

**Cross-questions:**
- **Where is a persona useful?** Support bots with a brand voice, tutors for kids, a formal assistant for legal text.
- **Why did `persona_playground.py` use temperature 0.7?** A little variety makes the personas sound natural instead of robotic.
- **Is the Lawyer persona real legal advice?** No. It only changes the style. The facts can still be wrong.

---

## 6. Temperature

**Basic: What does temperature do?**
It controls randomness. 0 picks the most likely words; higher values take more chances.

**Cross-questions:**
- **What did your tea-shop test show?** At 0: "Serenity Steep Lounge" three times. At 1.0: three different names.
- **When do you use low and when high?** Low (0) for facts, extraction and JSON. Higher (0.7–1.0) for creative writing, names and ideas.
- **Does temperature 0 guarantee the exact same answer every time?** Almost, not 100%. Tiny differences on the server side can still change a word.
- **Does a higher temperature make the model smarter?** No. Only more varied, and sometimes less accurate.

---

## 7. max_tokens and finish_reason

**Basic: What is `finish_reason`?**
Why the model stopped: `"stop"` means it finished naturally, `"length"` means it hit `max_tokens`.

**Cross-questions:**
- **Why check `finish_reason` in code?** A cut-off reply looks normal at a glance. With JSON, a cut-off breaks parsing.
- **The reply is empty and `finish_reason` is `"length"`. Why?** Hidden reasoning used the whole budget before the answer started. Raise `max_tokens`.

---

## 8. Hidden reasoning tokens

**Basic: Why did a one-sentence answer use 117 output tokens?**
`gpt-oss-120b` is a reasoning model. It thinks privately before answering, and those thinking tokens are billed as output.

**Cross-questions:**
- **Can you see the reasoning?** Not in `content`. You only see its cost in `completion_tokens`.
- **When would you choose a non-reasoning model?** For simple, high-volume tasks where speed and cost matter more than deep thinking.

---

## 9. Other parameters and the code

**Basic: Name other common parameters.**
`top_p` (another randomness control), `stop` (text that ends the reply), `n` (number of answers), `stream` (send tokens as they arrive, Day 4).

**Cross-questions:**
- **Should you change temperature and `top_p` together?** Usually change one, not both, so you know which one caused the effect.
- **Why open the file with mode `"a"` in `persona_playground.py`?** Append mode adds each run to the end instead of erasing earlier replies.
- **Why `encoding="utf-8"` when writing the file?** Windows' default encoding can't save characters like `’` or emoji.
