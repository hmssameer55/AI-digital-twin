# AI Digital Twin

A chatbot that answers questions about my career, as me. Visitors chat with it; when
it doesn't know an answer, or someone leaves their email, it pings my phone via Pushover.

Built in Week 1 of Ed Donner's *AI Engineer Agentic Track* course (based on the
[ed-donner/agents](https://github.com/ed-donner/agents) repo, MIT license).

## How it works

1. `context.py` builds a system prompt from `summary.txt` + `linkedin.pdf`.
2. `app.py` sends the chat to OpenAI with two tools attached.
3. If the model asks to call a tool, the app runs it, appends the result, and calls
   the model again — a plain `while` loop until it returns a normal answer.
4. `tools.py` has the two tools: `record_user_details` and `record_unknown_question`,
   both send a Pushover notification.
5. Gradio renders the chat UI.

## Run locally

```bash
cp .env.example .env        # fill in your keys
# add your own linkedin.pdf (LinkedIn → Profile → More → Save to PDF)
pip install -r requirements.txt
python app.py
```

`linkedin.pdf` is git-ignored because the export contains contact details.
