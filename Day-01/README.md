# Day 1: Set up and make your first call

**Build:** a script that prints a model reply.
**Real project:** Hello AI, which explains a topic you care about in 3 simple lines.
**Revise:** [revision_notes.md](revision_notes.md) has the flow diagram, key ideas and a recall quiz.

## Already done
- [x] Python 3.14 installed
- [x] Virtual environment `venv/` created in the main folder (shared by all 30 days)
- [x] `groq` and `python-dotenv` installed (provider: Groq, free tier)
- [x] `.env` and `.gitignore` created in the main folder

## Your steps
1. Get an API key: console.groq.com > API Keys > Create API Key. Copy it right away.
2. Open `.env` in the main folder and replace `paste-your-groq-key-here` with your key (no quotes or spaces).
3. Open a terminal in VS Code and activate the venv:
   ```powershell
   venv\Scripts\activate
   ```
   If you see "running scripts is disabled", run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` and try again.
4. Run your first program:
   ```powershell
   python Day-01\first.py
   ```
   You should see 3 lines explaining an API, then two numbers (tokens used).
5. Run the real project:
   ```powershell
   python Day-01\hello_ai.py
   ```

## Your turn (10 minutes)
1. Change the question in `first.py` to something about your hobby or subject.
2. Set `max_tokens=40` and watch the answer get cut off.
3. Ask for the answer "as a table", then "as a poem".
4. Compare the token numbers each time.

## If something breaks
| Error | Fix |
|---|---|
| `authentication_error` / 401 | Check the key in `.env` is complete, with no quotes |
| rate limit (429) | Free tier limit hit; wait a minute and retry |
| model not found / decommissioned | Copy a current model name from console.groq.com/docs/models |
| No module named 'groq' | Activate the venv first (look for `(venv)`) |

## Notes
Write what you learned here:
-
