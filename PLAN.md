# 30 days to your first AI apps

Build chatbot and RAG applications in about 1.5 to 2 hours a day.
Tick a day only when its build step runs on your machine.

> **Provider note:** the original plan uses Anthropic. This repo uses **Groq** (free tier, OpenAI-style `chat.completions` API), so every example is translated to Groq.

## Progress

| Phase | Days | Goal | Done |
|---|---|---|---|
| 1. LLM API basics | 1 to 5 | Call a model from Python and hold a conversation. | 1 / 5 |
| 2. Embeddings and vector search | 6 to 10 | Turn text into vectors and find similar meaning. | 0 / 5 |
| 3. RAG, the core skill | 11 to 17 | Answer questions from your own documents, with citations. | 0 / 7 |
| 4. Evaluation | 18 to 21 | Prove your RAG works. This is what gets you hired. | 0 / 4 |
| 5. Tool use and chat with a database | 22 to 25 | Let the model call your functions and query SQL. | 0 / 4 |
| 6. Ship it | 26 to 30 | Turn your projects into a deployed application you can show. | 0 / 5 |

**Overall: 1 / 30 days**

---

## Phase 1: LLM API basics

- [x] **Day 1: Set up and make your first call** ([Day-01](Day-01/))
  Install Python, VS Code, venv, get an API key, save it in `.env`, run `first.py`.
  - **Build:** Script that prints a model reply.
  - **Real project:** Hello AI: explain a topic you care about (GST, cricket rules, a school chapter) in 3 simple lines.

- [ ] **Day 2: Messages, system prompts, parameters** ([Day-02](Day-02/))
  Learn roles (system/user/assistant), max_tokens, temperature and tokens. Ask the same question under 3 different system prompts and compare.
  - **Build:** Notes file comparing 3 system prompts.
  - **Real project:** Persona playground: ask one question as a teacher, a lawyer and a friend, and save all three replies in a text file to compare.

- [ ] **Day 3: Prompt engineering and JSON output**
  Write clear instructions, add 2-3 examples, and force structured JSON output. Parse it safely in Python.
  - **Build:** Function that extracts name, date and amount from messy text as JSON.
  - **Real project:** Order extractor: paste a messy WhatsApp order ("2 kg rice, 1 oil bottle, sugar 5kg") and get clean JSON with item, quantity and unit.

- [ ] **Day 4: Streaming and conversation memory**
  Stream tokens as they arrive and keep a messages list so the bot remembers earlier turns.
  - **Build:** Chat loop in the terminal with streaming.
  - **Real project:** Typing-effect chatbot: replies appear word by word, and the bot remembers your name from 3 messages ago.

- [ ] **Day 5: Mini project: CLI chatbot**
  Add a persona with a system prompt, save every conversation to SQLite, and reload the last chat on start.
  - **Build:** Project 0: CLI chatbot with SQLite history on GitHub.
  - **Real project:** Study Buddy: a terminal tutor for one subject that remembers yesterday's chat.

> **Phase project: Study Buddy (terminal chatbot)** (Beginner)
> A tutor chatbot with a personality that remembers earlier messages and saves chats.
> 1. Ask the model a question from Python (Day 1). 2. System prompt for a patient tutor (Day 2-3). 3. Messages list + streaming (Day 4). 4. Save and reload chats with SQLite (Day 5).
> **Works when:** you close it, reopen tomorrow, and the tutor remembers what you studied.

---

## Phase 2: Embeddings and vector search

- [ ] **Day 6: What embeddings are**
  Embed 10 sentences with sentence-transformers. Compare scores for similar and unrelated sentences.
  - **Build:** Notebook printing similarity scores.
  - **Real project:** Meaning matcher: "how do I reset my password" is closer to "forgot login" than to "opening hours".

- [ ] **Day 7: Similarity search from scratch**
  Implement cosine similarity with numpy and return the top 3 matches. No library yet.
  - **Build:** `search(query, k)` over 20 sentences.
  - **Real project:** FAQ finder: type a question in your own words and get the closest of 20 FAQ answers, with a score.

- [ ] **Day 8: Chunking documents**
  Split long text by characters, then by paragraphs, with overlap. See how chunk size changes results.
  - **Build:** Chunker function with size and overlap settings.
  - **Real project:** Chunk viewer: print a Wikipedia article as numbered chunks with overlap, and see where a sentence gets cut.

- [ ] **Day 9: Vector database: Chroma**
  Store chunks and metadata in Chroma, persist to disk, and query with filters.
  - **Build:** Ingest script plus query script using Chroma.
  - **Real project:** Notes search: save 30 of your own notes in Chroma and find the right one with a vague question.

- [ ] **Day 10: Mini project: semantic search**
  Index 20 text or markdown files and build a command-line search showing the best chunks and file names.
  - **Build:** Project 1a: semantic search tool. Optional: redo storage in pgvector.
  - **Real project:** Docs search engine: search 20 markdown files and show the file name beside each result.

> **Phase project: Notes Search Engine** (Beginner to intermediate)
> Search 20-30 files by meaning and show the file and matching paragraph.
> Embeddings (Day 6) → cosine ranking (Day 7) → chunking (Day 8) → Chroma + search command (Day 9-10).
> **Works when:** "how do I stay focused" finds the note titled "Pomodoro technique".

---

## Phase 3: RAG, the core skill

- [ ] **Day 11: Load PDFs and clean text**
  Extract text per page with pypdf, keep page numbers as metadata, remove headers and footers.
  - **Build:** Loader returning `(text, source, page)`.
  - **Real project:** Resume or textbook reader: real PDF, page by page, into a clean list with page numbers.

- [ ] **Day 12: Build the ingestion pipeline**
  Load, chunk, embed and store in one command. Re-running must be safe (no duplicates).
  - **Build:** `ingest.py` that processes a folder of PDFs.
  - **Real project:** Knowledge base builder: drop 5 PDFs in a folder, run one command, all searchable.

- [ ] **Day 13: Retrieve, then generate**
  Retrieve top-k chunks, put them in the prompt, and ask the model to answer only from them.
  - **Build:** `ask(question)` returning an answer.
  - **Real project:** Ask-my-PDF: ask "what is the notice period?" of a real contract.

- [ ] **Day 14: Citations and "I don't know"**
  Return source file and page with each answer. Refuse when the context lacks the answer.
  - **Build:** Answers with sources, plus a refusal test question.
  - **Real project:** Trustworthy answerer: every answer ends with (file, page); off-topic questions get "I could not find this".

- [ ] **Day 15: Tune retrieval**
  Experiment with chunk size, overlap, top-k and metadata filters. Record how quality changed.
  - **Build:** Tuning log in your README.
  - **Real project:** Tuning lab: chunk size 200/500/1000 vs how often the right chunk is found.

- [ ] **Day 16: Hybrid search and reranking**
  Combine BM25 keyword scores with vector scores. Optionally rerank top 20 down to 5.
  - **Build:** Hybrid retriever you can switch on or off.
  - **Real project:** Product-manual search: exact model numbers work (keyword) and so does "phone gets hot" (meaning).

- [ ] **Day 17: Project 1: chat with your PDFs**
  Streamlit chat UI with file upload, chat history and an expandable sources section.
  - **Build:** Project 1: working PDF chatbot app.
  - **Real project:** Upload a PDF in the browser, chat, and click to see the exact source passages.

> **Phase project: Chat with PDFs** (Intermediate)
> Upload a PDF, ask questions, get cited answers, refuse what the PDF can't answer.
> **Works when:** a stranger can use it without instructions and every answer shows its source page.

---

## Phase 4: Evaluation

- [ ] **Day 18: Build a test set**
  25 questions with the correct answer and page, including 5 the documents cannot answer.
  - **Build:** `eval_set.json` with 25 items.

- [ ] **Day 19: Measure retrieval**
  Check whether the right chunk appears in the top-k. Report the hit rate.
  - **Build:** Script printing retrieval hit rate ("Right chunk in top 3: 21 of 25 (84%)").

- [ ] **Day 20: Measure answer quality**
  Model as a judge: is the answer correct and grounded only in the context? Score all 25.
  - **Build:** Script printing correctness and faithfulness scores, saved to CSV.

- [ ] **Day 21: Improve with evidence**
  Change one thing (chunking, hybrid, prompt), re-run evals, record before and after.
  - **Build:** Results table in README ("Hybrid search raised answers found from 72% to 88%").

> **Phase project: RAG Report Card** (Intermediate)
> **Works when:** your README has a before/after numbers table.

---

## Phase 5: Tool use and chat with a database

- [ ] **Day 22: Function calling basics**
  Define a tool (`get_weather`, `lookup_order`), let the model request it, run it, return the result.
  - **Real project:** Order-status assistant: "where is order 1042?" calls `lookup_order()`.

- [ ] **Day 23: Text-to-SQL**
  Give the model your schema and example queries; it returns SQL for a plain-English question.
  - **Real project:** "Which 3 customers spent the most?" on the Chinook sample database.

- [ ] **Day 24: Make SQL safe**
  Read-only user, SELECT only, row limit, show SQL before running.
  - **Build:** Validator that blocks DROP, DELETE and UPDATE.

- [ ] **Day 25: Project 2: chat with your database**
  Tool use + text-to-SQL: user asks, model queries, model explains the result.
  - **Build:** Project 2: database chatbot with UI that shows the SQL used.

> **Phase project: Ask My Data** (Intermediate)
> **Works when:** "Top 5 customers by spend" works and "drop table" is refused.

---

## Phase 6: Ship it

- [ ] **Day 26: Wrap it in FastAPI** — `api.py` with `/ask` and `/health`, tested on `/docs`.
- [ ] **Day 27: Connect frontend and stream** — UI calls the API and streams the answer; input validation.
- [ ] **Day 28: Logging, caching and errors** — log question, latency, tokens; cache repeats; retries for timeouts and rate limits.
- [ ] **Day 29: Deploy** — Docker or direct deploy (Render / Hugging Face Spaces), API key as a secret, public link.
- [ ] **Day 30: Polish and publish** — README (problem, architecture, eval results, demo link), 1-minute demo video, resume and LinkedIn.

> **Capstone: Deployed AI Assistant** (Intermediate)
> **Works when:** you can send one link to a recruiter and it works on their phone.

---

## After the 30 days: projects, basic to advanced

| # | Project | Level | Start after | Stretch goal |
|---|---|---|---|---|
| 1 | Smart Q&A chatbot with memory | Basic | Day 5 | /reset command, choice of personalities |
| 2 | Resume parser and summarizer | Basic | Day 3 | PDF resumes, save to CSV/SQLite |
| 3 | WhatsApp or email reply writer | Basic | Day 3 | Learn your style from 5 samples |
| 4 | FAQ finder with semantic search | Basic-Int | Day 7 | Confidence score, "not sure" threshold |
| 5 | Chat with PDFs | Intermediate | Day 13 | Many PDFs, filter by document |
| 6 | Customer support bot with escalation | Intermediate | Day 22 | Log unanswered questions |
| 7 | Chat with your database | Intermediate | Day 24 | Chart for numbers over time |
| 8 | Resume screener with RAG | Intermediate | Day 16 | Metadata filters (experience, location) |
| 9 | Study assistant: notes to quiz | Intermediate | Day 17 | Spaced repeats of wrong answers |
| 10 | Meeting notes assistant | Int-Advanced | Day 25 | Deploy with team logins |
| 11 | Research agent with tools | Advanced | Day 25 | Evals that check tool choice |

One project every 1-2 weeks, each with a README, screenshots and a demo link.
