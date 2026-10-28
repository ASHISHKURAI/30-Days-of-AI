# Day 1: basic questions and cross-questions

Each topic starts with a **basic question**. The **cross-questions** under it are the follow-ups an interviewer asks to check that you really understand it. Answer out loud before you read the answer.

---

## 1. Virtual environment (venv)

**Basic: Why do we need a venv?**
A venv is a private folder of Python packages for one project. Without it, every project shares one global set of packages, and they start to clash.

**Benefits:**
- **No version clashes:** project A can use `groq 0.9` while project B uses `groq 0.30`.
- **Clean system Python:** you never break Windows' or other tools' packages.
- **Reproducible:** `pip freeze > requirements.txt` lists exactly what this project needs, so anyone can rebuild it.
- **Easy reset:** if it breaks, delete `venv/` and recreate it. Nothing else is affected.

**Cross-questions:**
- **What happens if you don't use one?** Packages install globally. Upgrading a library for one project can silently break another.
- **How do you know the venv is active?** The terminal line starts with `(venv)`, and `where python` points inside `venv\Scripts\`.
- **Why is `venv/` in `.gitignore`?** It's large, specific to your machine and OS, and can be rebuilt from `requirements.txt`. You share the recipe, not the kitchen.
- **You installed `groq`, but you get `No module named 'groq'`. Why?** You installed it in one environment and are running Python from another, usually because the venv isn't active.
- **venv vs conda?** Both isolate packages. venv is built into Python and is enough here; conda also manages non-Python dependencies and Python versions.
- **Does a venv isolate the Python version too?** No. It uses the Python it was created with. To use another version, create the venv with that Python.

---

## 2. API

**Basic: What is an API?**
A way for your code to use someone else's program. You send a request in an agreed format and get a response back.

**Cross-questions:**
- **Why call an LLM through an API instead of running it locally?** A 120B-parameter model needs huge GPUs. The API gives you that power for a few rupees per million tokens, with no setup.
- **What travels in the request?** The model name, your messages and settings like `max_tokens`, sent as JSON over HTTPS.
- **Is an API call like a normal function call?** No. It goes over the network, so it can be slow, fail, time out or hit rate limits. Real apps must handle errors.

---

## 3. API key

**Basic: What is an API key?**
A secret string that proves the request comes from you. Groq uses it for billing and limits.

**Cross-questions:**
- **Why not write the key directly in `first.py`?** The code goes to GitHub, and bots scan GitHub for leaked keys within minutes.
- **What do you do if the key leaks?** Delete it in the Groq console right away and create a new one. Removing it from the code isn't enough, because it stays in Git history.
- **How is the key handled in production?** As an environment variable or in a secrets manager on the server, never in the code.

---

## 4. `.env` and `load_dotenv()`

**Basic: What does `load_dotenv()` do?**
It reads `.env` and puts each `NAME=value` line into the environment variables of the running program.

**Cross-questions:**
- **How does `Groq()` find the key when you never pass it?** The client reads the `GROQ_API_KEY` environment variable by itself.
- **What if `.env` is missing?** `load_dotenv()` doesn't fail. The error appears later, when `Groq()` can't find a key.
- **Why does `.env` have no quotes or spaces?** Extra characters become part of the key, which then fails with a 401 error.

---

## 5. `.gitignore`

**Basic: What is `.gitignore`?**
A list of files Git must never track or upload. Yours lists `.env`, `venv/` and `__pycache__/`.

**Cross-questions:**
- **You added `.env` to `.gitignore` after committing it. Is it safe?** No. It's already in the history. Remove it from tracking (`git rm --cached .env`) and rotate the key.
- **Why ignore `__pycache__/`?** It holds compiled bytecode that Python regenerates automatically. It is noise in the repo.

---

## 6. `requirements.txt`

**Basic: What is `requirements.txt` for?**
It lists the packages the project needs, so anyone can install them with `pip install -r requirements.txt`.

**Cross-questions:**
- **Why pin versions like `groq==0.30.0`?** So everyone gets the same versions and a future release can't break your code silently.
- **How does it relate to the venv?** The venv is where packages live on your machine; `requirements.txt` is how you recreate that venv anywhere.

---

## 7. The client and the call

**Basic: Walk me through `first.py`.**
Load `.env`, create the `Groq()` client, call `client.chat.completions.create()` with a model, `max_tokens` and messages, then print the answer and the token counts.

**Cross-questions:**
- **Why create the client once and not inside every function?** It holds the key and the network connection. Reusing it is faster and cleaner.
- **Why `reply.choices[0].message.content`?** `choices` is a list (you could ask for several answers). `[0]` is the first one, and `.message.content` is its text.
- **What if the model name is wrong or retired?** You get a "model not found" or "decommissioned" error. Copy a current name from the Groq models page.

---

## 8. Tokens and cost

**Basic: What is a token?**
A chunk of text, roughly ¾ of an English word. Models read and write tokens, and you pay per token.

**Cross-questions:**
- **What is the difference between `prompt_tokens` and `completion_tokens`?** `prompt_tokens` is what you sent; `completion_tokens` is what the model wrote, including hidden reasoning.
- **Do Hindi or Hinglish words cost the same?** Usually more. Non-English text often splits into more tokens per word.
- **How do you cut cost?** Shorter prompts, a sensible `max_tokens`, a smaller model for easy tasks, and not resending history you don't need.

---

## 9. `max_tokens`

**Basic: What does `max_tokens` do?**
It sets the most tokens the model may write for one reply.

**Cross-questions:**
- **Is it your account balance?** No. It limits one reply only.
- **You set `max_tokens=40` and got an empty answer. Why?** `gpt-oss-120b` reasons privately first. All 40 tokens went on reasoning, leaving nothing for the visible answer.
- **Why not always set it very high?** A runaway reply costs more and takes longer. Set it to what the task needs, with room for reasoning.

---

## 10. Errors

**Basic: What errors did you hit, and how did you fix them?**
Name a real one: for example, `UnicodeEncodeError` on Windows, fixed with `sys.stdout.reconfigure(encoding="utf-8")`.

**Cross-questions:**
- **What does a 401 mean?** Bad or missing key.
- **What does a 429 mean?** Rate limit. You sent too many requests or tokens per minute. Wait and retry, ideally with a growing delay (backoff).
- **Why did printing fail on Windows but not on Mac?** The Windows terminal used an old encoding that couldn't show characters like `’` or emoji. UTF-8 can.
