# Day 1 Interview Questions: LLM API Basics

Questions an interviewer might ask about what you built on Day 1: calling an LLM from Python, keeping the API key safe, and reading the response.
Answer in your own words. Say the short version first, then add detail if they ask.

---

## Section A: LLM and API basics

### 1. What is an API?
**Answer:** An API (Application Programming Interface) is a set of rules that lets one program talk to another. My Python script sends a request to Groq's server over the internet and gets the model's answer back as data, without knowing how the server works inside.
*Example:* It's like a restaurant menu. You order from the menu (the request) and the kitchen sends the dish (the response) without you seeing the cooking.

### 2. What is an LLM?
**Answer:** An LLM (Large Language Model) is an AI model trained on a huge amount of text to predict the next token. Repeating that prediction lets it answer questions, write, summarize and code. Examples are GPT, Llama, Claude and Gemini.

### 3. Why call an LLM through an API instead of running it on your own computer?
**Answer:**
- Big models need powerful GPUs that a normal laptop doesn't have.
- The provider handles hosting, scaling and updates.
- You pay only for what you use (or use a free tier).
- The trade-off is that your data goes to a third party, you depend on the internet, and there's a cost per token.

### 4. Which provider did you use, and why?
**Answer:** I used Groq with the `openai/gpt-oss-120b` model. Groq has a free tier and is very fast. Its API follows the OpenAI format (`chat.completions`), so the same code style works with OpenAI and many other providers.

---

## Section B: API keys and security

### 5. What is an API key?
**Answer:** A secret string that identifies me to the provider. It tells the server who is making the request and which account to bill or rate-limit. Without a valid key, the server returns `401 Invalid API Key`.

### 6. How did you store your API key, and why not write it in the code?
**Answer:** I put it in a `.env` file (`GROQ_API_KEY=...`) and load it with `python-dotenv`. If the key were written in the code, it would leak when I push to GitHub. Bots scan GitHub for keys within minutes and can run up charges on your account.

### 7. What does `load_dotenv()` do?
**Answer:** It reads the `.env` file and puts each line into the program's environment variables. Then `Groq()` finds `GROQ_API_KEY` automatically with `os.environ`. By default it does **not** overwrite an environment variable that is already set.

### 8. What is `.gitignore` and what did you put in it?
**Answer:** It lists the files Git should never track or commit. I added `.env` (the secret key), `venv/` (big and machine-specific) and `__pycache__/` (Python's generated files).

### 9. What would you do if your API key leaked?
**Answer:** Revoke it in the provider's console right away, create a new one, and update `.env`. Removing it from the code isn't enough, because it stays in the Git history.

### 10. How would you handle the key in production?
**Answer:** Not with a `.env` file in the repo. I'd use the hosting platform's secrets or environment-variable settings (for example Render, Hugging Face Spaces or GitHub Actions secrets), or a secrets manager such as AWS Secrets Manager.

---

## Section C: Python setup

### 11. What is a virtual environment and why use one?
**Answer:** A private folder of Python libraries for one project. It keeps one project's versions from breaking another's.
```powershell
python -m venv venv       # create
venv\Scripts\activate     # activate on Windows; you then see (venv)
```

### 12. What does `pip install groq python-dotenv` do?
**Answer:** It downloads and installs two libraries into the active environment: `groq`, the official client for calling Groq's API, and `python-dotenv`, which reads the `.env` file.

### 13. What is `requirements.txt` for?
**Answer:** It lists the project's libraries so anyone can recreate the setup with `pip install -r requirements.txt`.

---

## Section D: The code

### 14. Walk me through your Day 1 script.
```python
from dotenv import load_dotenv
from groq import Groq

load_dotenv()                     # 1. load key from .env
client = Groq()                   # 2. create the client (uses GROQ_API_KEY)

reply = client.chat.completions.create(   # 3. send the request
    model="openai/gpt-oss-120b",
    max_tokens=300,
    messages=[{"role": "user", "content": "Explain what an API is in 3 simple lines."}],
)

print(reply.choices[0].message.content)                      # 4. answer text
print(reply.usage.prompt_tokens, reply.usage.completion_tokens)  # 5. token usage
```
**Answer:** Load the key, create a client, send a list of messages with a model name and a token limit, then read the answer text and the token usage from the response.

### 15. What is a "client" here?
**Answer:** An object that holds the connection settings (API key, base URL, timeouts, retries) and has methods like `chat.completions.create()` to call the API, so I don't have to write HTTP requests by hand.

### 16. What is the `messages` list?
**Answer:** The conversation sent to the model. Each item has a `role` and `content`. The roles are:
- `system`: instructions for how the model should behave (covered on Day 2)
- `user`: what the person says
- `assistant`: what the model said earlier

The model has no memory between calls, so to hold a conversation you send the whole history every time.

### 17. Why `reply.choices[0].message.content`?
**Answer:** The API can return more than one answer (choices), so `choices` is a list. `[0]` takes the first one, `.message` is the assistant's message, and `.content` is its text. (In the Anthropic SDK the same thing is `reply.content[0].text`.)

### 18. Why must you pass a model name, and what happens if it's wrong?
**Answer:** A provider hosts many models with different quality, speed and price. A wrong or retired name returns `404 model_not_found`. That happened to me with `llama-3.3-70b-versatile`. I fixed it by listing the available models with `client.models.list()` and switching to `openai/gpt-oss-120b`.

---

## Section E: Tokens, limits and cost

### 19. What is a token?
**Answer:** A small piece of text that the model reads and writes, often part of a word. In English, one token is roughly 4 characters or three quarters of a word. Models are priced and limited in tokens.

### 20. What are input tokens and output tokens?
**Answer:**
- **Input (prompt) tokens:** everything I send, including the system prompt, the history and the question.
- **Output (completion) tokens:** everything the model generates.

My first call used `82` in and `129` out. Output tokens usually cost more than input tokens.

### 21. What does `max_tokens` do?
**Answer:** It's the maximum number of tokens the model may generate for **one** reply, not my account balance. When the limit is reached, the answer stops mid-sentence. A lower limit means lower cost and faster replies, but also the risk of a cut-off answer.

### 22. You set `max_tokens=40` and got an empty answer. Why?
**Answer:** `gpt-oss-120b` is a **reasoning model**: it thinks internally before answering, and that hidden reasoning counts toward `max_tokens`. The usage showed `40` output tokens, all spent on reasoning, with nothing left for the visible answer. The fix is to raise `max_tokens` or lower the reasoning effort.
*This is a good answer to give because it shows you debugged something real.*

### 23. How would you reduce the cost of LLM calls?
**Answer:** Write shorter prompts, set a sensible `max_tokens`, use a smaller or cheaper model for simple tasks, cache answers to repeated questions, and avoid sending conversation history that isn't needed.

---

## Section F: Errors and debugging

### 24. What errors did you hit, and how did you fix them?
| Error | Cause | Fix |
|---|---|---|
| `401 Invalid API Key` | `.env` was edited but not saved, so the placeholder was still on disk | Saved the file and checked the key |
| `404 model_not_found` | The model had been retired | Listed the models and switched to `openai/gpt-oss-120b` |
| Empty answer | `max_tokens` was too small for a reasoning model | Raised `max_tokens` |
| `429 rate limit` (possible) | The free tier allows only so many requests per minute | Wait and retry, ideally with exponential backoff |

### 25. What are rate limits?
**Answer:** Caps the provider sets on requests or tokens per minute or per day, to share capacity fairly. Going over returns `429`. In real apps you handle it by retrying with exponential backoff (wait 1s, then 2s, then 4s, and so on), for example with the `tenacity` library.

### 26. Is an LLM API call fast and reliable like a normal function call?
**Answer:** No. It goes over the network, can take seconds, and can fail with timeouts, rate limits or server errors. Production code needs timeouts, retries, error handling and logging (covered on Day 28).

---

## Quick revision: one-line answers
- **API:** the way programs talk to each other.
- **API key:** a secret that identifies you; keep it in `.env` and list `.env` in `.gitignore`.
- **venv:** separate libraries for each project.
- **Client:** the object that makes the API calls for you.
- **messages:** a list of `{role, content}`; the model is stateless, so you send the history each time.
- **Token:** about three quarters of a word; it's what you're billed and limited on.
- **max_tokens:** the length limit for one reply; reasoning models spend some of it thinking.
- **401 / 404 / 429:** bad key / bad model / too many requests.
