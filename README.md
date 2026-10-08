# My Developer Toolbox

Seven Streamlit tools, compatible with Python 3.10. Local-first portfolio project.

## Windows setup

Extract this ZIP. Copy its contents into your blank-app project (back up your old streamlit_app.py first). Keep core.py beside streamlit_app.py.

In PowerShell, from the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
```

Edit .streamlit/secrets.toml with your own Groq key. Never commit this file.

```toml
GROQ_API_KEY = "your-real-key"
GROQ_TEXT_MODEL = "llama-3.3-70b-versatile"
GROQ_VISION_MODEL = "qwen/qwen3.8-27b"
```

Model IDs are configurable because Groq availability changes. Check https://console.groq.com/docs/models and https://console.groq.com/docs/vision if a model is unavailable to your account.

Start:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Open http://localhost:8501. Stop with Ctrl+C. To restrict your local server to your own computer, append `--server.address 127.0.0.1`.

## Try each page

1. AI Chatbot: add your key, ask a question, clear the conversation.
2. PDF Q&A: upload a text PDF, ask about a named topic, inspect the source excerpts. Uses keyword-based chunk retrieval, not exhaustive document review. Up to 100 pages, 10 MB; extraction capped at 50,000 characters per page. Scanned PDFs and encrypted PDFs are unsupported.
3. Invoice vs PO: built-in sample includes matched items, quantity/price mismatches, a missing item, and an extra item. Upload CSV/XLSX with item_code,quantity,unit_price. Item codes must be unique; casing and spaces are normalized. Currency/tax must already be comparable. No PDF invoice parsing, partial-delivery reconciliation, or AutoCount API calls.
4. Dashboard: try sample data or upload CSV/XLSX; choose filter, grouping, value, sum/average, and bar/line chart.
5. Login & Records: create a username and password (12+ characters), save notes/amounts, log out and back in.
6. Image Text Extractor: upload PNG/JPEG, extract via Groq vision, download text. English, Chinese, Malay or auto-detect. AI transcription can be inaccurate. Images resized to 2000px maximum dimension.
7. Database Manager: log in, search your own records, update, export, and confirm deletion. There is no arbitrary SQL console or access to other users' records.

AI calls submit your prompt, selected PDF excerpts, or image to Groq. Conversation/upload state is session-only. Accounts and records live in data/toolbox.db. Back up this file for local persistence. Passwords use salted scrypt; SQL is parameterized and record operations scope to the signed-in owner. This login is a learning implementation, with session-only throttling and no recovery/verification or global abuse protection.

## Public demo via Streamlit Community Cloud

1. Push the source files and requirements.txt to GitHub. Do not push secrets.toml, data/, or .venv/.
2. Go to https://share.streamlit.io and create an app from your repository; entrypoint: streamlit_app.py. Select a compatible Python version in advanced settings.
3. Paste the TOML secrets into the app's Secrets settings, then deploy.
4. Share the provided URL after checking the app's access settings.

No public deployment has been performed by this deliverable. This app can run as a public portfolio demo, but do not rely on it for permanent cloud accounts or private production data: Community Cloud local files are not guaranteed to persist. Use an external durable database and production authentication before real multi-user use. Anyone with access to the AI pages can consume the configured Groq key's quota. Set Groq usage limits, or keep the app private for testing.

## Validation

See test_toolbox.py. Run `python test_toolbox.py` after installation. Tests cover navigation smoke checks, record isolation, password authentication, comparison validation, and mocked AI request construction. Mocked calls do not verify the real key or Groq service.

python -m streamlit run streamlit_app.py