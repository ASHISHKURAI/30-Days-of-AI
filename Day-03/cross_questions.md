# Day 3: basic questions and cross-questions

> **Preview.** Written before you build Day 3. After you run the scripts, add your own examples to the answers.

Each topic starts with a **basic question**. The **cross-questions** under it are the follow-ups an interviewer asks to check that you really understand it. Answer out loud before you read the answer.

---

## 1. Prompt engineering

**Basic: What is prompt engineering?**
Writing instructions so the model gives the output you need, reliably: a clear role, task, rules, output format and examples.

**Cross-questions:**
- **What makes a prompt "clear"?** One task, specific rules, the exact output format, and what to do when information is missing.
- **Why say "never guess" or "use null if missing"?** Without it, the model fills gaps with a confident guess, such as an invented date.
- **Should the rules go in the system or the user message?** Fixed rules go in `system`. The changing input goes in `user`.
- **How do you know a prompt change made things better?** Test it on the same set of example inputs before and after. Don't judge it from one try.

---

## 2. Zero-shot vs few-shot

**Basic: What is few-shot prompting?**
Giving the model 2–3 examples of input with the exact output you want, before the real input.

**Cross-questions:**
- **What is zero-shot?** Instructions only, no examples.
- **How do examples go into the messages list?** As fake `user` and `assistant` pairs between the system message and the real input.
- **Why only 2–3 examples?** Each example costs tokens on every call, and after a few the gains get smaller.
- **What makes a good example?** Variety, including a tricky case, such as one with a missing value that should return `null`.
- **Can bad examples hurt?** Yes. The model copies their mistakes too.

---

## 3. Why JSON?

**Basic: Why ask the model for JSON instead of plain text?**
Code can't reliably read a paragraph, but `json.loads` turns JSON into a Python dict you can use directly.

**Cross-questions:**
- **Why not just split the text with string methods?** The wording changes every time, so string parsing breaks. JSON has a fixed shape.
- **What does "structured output" mean?** Output with a fixed format and fixed keys, so code can consume it.

---

## 4. JSON mode

**Basic: What does `response_format={"type": "json_object"}` do?**
It forces the reply to be valid JSON.

**Cross-questions:**
- **Does it guarantee your keys and types?** No. Only valid JSON syntax. Your code must still check the keys and types.
- **What is the difference from `json_schema` mode?** `json_schema` with `"strict": true` makes supported models (like gpt-oss) follow your exact schema.
- **Why must the top level be an object?** JSON mode returns an object. To return a list, wrap it: `{"items": [...]}`.
- **What if the model fails to produce valid JSON?** Groq returns a 400 error, `json_validate_failed`. Catch `groq.BadRequestError` and retry.

---

## 5. Parsing safely

**Basic: How do you parse the reply safely?**
Wrap `json.loads` in `try/except`, then check the keys and types before using the data.

**Cross-questions:**
- **Which exception does `json.loads` raise?** `json.JSONDecodeError`.
- **Why retry only once?** One retry fixes most random failures. More retries waste money and time if the prompt itself is the problem.
- **What do you return after the retry also fails?** `None` (and log it), so the app keeps running instead of crashing.
- **Why might the JSON be cut off?** `max_tokens` ran out, often because of hidden reasoning. Check `finish_reason == "length"`.
- **What if the reply is wrapped in ```` ```json ```` fences?** That happens without JSON mode. Turn JSON mode on, or strip the fences before parsing.

---

## 6. Validation

**Basic: Why validate after `json.loads` works?**
Valid JSON can still be wrong: missing keys, extra keys, or `"2500"` as a string instead of the number `2500`.

**Cross-questions:**
- **How do you check the types?** With `isinstance`, for example `isinstance(data["amount"], (int, float, type(None)))`.
- **Is there a library for this?** Yes: Pydantic. You define a model class, and it validates and converts the data for you.
- **Should you trust a value just because it's the right type?** No. A real-looking date can still be invented. That's why the prompt needs the null rule.

---

## 7. Temperature for extraction

**Basic: Why use `temperature=0` for extraction?**
The same message should give the same JSON every time.

**Cross-questions:**
- **What happens at temperature 1.0?** Key names, number formats and guesses can change from run to run.
- **Is there any task where you'd raise it?** Not for extraction. Only for creative output.

---

## 8. Real project: order extractor

**Basic: How does the WhatsApp order extractor work?**
It sends a messy order like "2 kg rice, 1 oil bottle, sugar 5kg" with a JSON prompt and examples, and gets back `{"items": [{"item", "quantity", "unit"}, ...]}`.

**Cross-questions:**
- **Why should quantity be a number, not a string?** So code can add, compare and multiply it, for example to total the bill.
- **How do you handle "sugar 5kg" vs "5 kg sugar"?** Show both word orders in the examples. The model learns that the order doesn't matter.
- **What about Hinglish orders like "do kilo chawal"?** Add one Hinglish example. The model can translate to `{"item": "rice", "quantity": 2, "unit": "kg"}`.
- **What if an item has no quantity, like "some salt"?** Return `"quantity": null` and let a human or the app ask for it.
- **How do you make units consistent?** List the allowed units in the prompt (`kg`, `g`, `litre`, `piece`, `bottle`, `packet`) and check them in code.

---

## 9. Linking back to Days 1 and 2

**Cross-questions:**
- **Which Day 2 idea makes few-shot work?** You can write `assistant` messages yourself.
- **Which Day 1/Day 2 setting can break your JSON?** `max_tokens`. Too small, and the JSON is cut off.
- **Does JSON mode change how you pay?** No. You still pay for input and output tokens, including hidden reasoning.
