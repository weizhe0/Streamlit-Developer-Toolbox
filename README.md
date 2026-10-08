# 🧰 Developer Toolbox

A web application that brings AI, document processing, data analysis,
and personal record management together in one place.

Users can chat with AI, ask questions about PDFs, compare invoices
against purchase orders, explore data, extract text from images,
and manage their own saved records.

Built with Python, Streamlit, Groq, Pandas, and SQLite.

---

## Features

- **AI chatbot** — ask questions through a conversational interface
  powered by Groq, with conversation history during the session.
- **PDF Q&A** — upload a text-based PDF and ask questions about its
  contents; answers include page references and source excerpts.
- **Invoice vs PO comparison** — compare item codes, quantities, and
  unit prices from CSV or Excel files; identify missing items,
  extra items, and differences.
- **Interactive dashboard** — upload data, filter records, group
  values, and display bar or line charts.
- **Login and personal records** — create an account, sign in, and
  save personal notes or expenses.
- **Image text extraction** — extract visible text from PNG or JPEG
  images using Groq vision, with a text download option.
- **Database management** — search, edit, export, and delete records
  belonging to the signed-in user.
- **Custom interface** — gradient background, dark sidebar,
  rounded panels, and consistent navigation.

---

## Tech stack

| Layer | Technology |
| ----- | ---------- |
| Interface | Streamlit |
| Language | Python |
| AI | Groq Python SDK |
| Data processing | Pandas |
| Database | SQLite |
| PDF processing | pypdf |
| Image processing | Pillow |
| Excel support | openpyxl |
| Styling | Custom CSS through `theme.py` |

---

## Getting started

### Prerequisites

- Python 3.10+
- A Groq API key for AI features
- Internet access for Groq requests

The invoice checker, dashboard, and personal record tools can run
without an AI key.

### 1. Download the project

Clone this repository using its GitHub URL, or download and extract
the ZIP.

Open a terminal in the project folder.

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

On Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On macOS or Linux:

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create `.streamlit/secrets.toml` in the project folder:

```toml
GROQ_API_KEY = "your-groq-api-key"
GROQ_TEXT_MODEL = "openai/gpt-oss-120b"
GROQ_VISION_MODEL = "qwen/qwen3.8-27b"
```

Use model IDs available to your Groq account. Model availability
may change.

The real `secrets.toml` file must not be committed to GitHub.

### 5. Run the application

On Windows:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

On macOS or Linux:

```bash
python -m streamlit run streamlit_app.py
```

Open **http://localhost:8501** in your browser.

Press **Ctrl + C** in the terminal to stop the application.

---

## Configuration

| Setting | Location | Purpose |
| ------- | -------- | ------- |
| `GROQ_API_KEY` | `.streamlit/secrets.toml` | Authenticate Groq requests |
| `GROQ_TEXT_MODEL` | `.streamlit/secrets.toml` | Model for chatbot and PDF Q&A |
| `GROQ_VISION_MODEL` | `.streamlit/secrets.toml` | Model for image text extraction |
| Theme colours | `.streamlit/config.toml` | Streamlit interface colours |
| Custom styling | `theme.py` | Background, sidebar, panels, and buttons |
| `TOOLBOX_DB_PATH` | Environment variable | Optional custom database path |

By default, accounts and records are stored in `data/toolbox.db`.
The database is created when account or record features are used.

---

## Project structure

```text
.streamlit/
  config.toml              Theme and upload settings
  secrets.toml.example     Example configuration without a real key
core.py                    Authentication, database, and comparison logic
streamlit_app.py           Main application and page navigation
theme.py                   Custom interface styling
requirements.txt           Python dependencies
test_toolbox.py            Automated checks
README.md                  Project documentation
.gitignore                 Excludes secrets and generated files
data/                      Local database; generated and git-ignored
```

---

## Invoice comparison input

Both files require these columns:

| Column | Description |
| ------ | ----------- |
| `item_code` | Unique item identifier |
| `quantity` | Item quantity |
| `unit_price` | Price per unit |

Example:

```csv
item_code,quantity,unit_price
ITEM-A,10,20.00
ITEM-B,5,40.00
ITEM-C,2,15.00
```

Item codes are compared after trimming spaces and normalising case.
Duplicate item codes must be combined before comparison.

The two files must use the same currency and tax basis.

Built-in sample data is available for trying the comparison tool
and dashboard.

---

## Testing

Run the included checks:

```powershell
python test_toolbox.py
```

The checks cover:

- Page navigation
- Password authentication
- Separation of records between users
- Invoice comparison and input validation
- Chatbot request construction using a mocked Groq response

Mocked AI tests do not verify live Groq responses or API credentials.

---

## Deployment

The application can be hosted using Streamlit Community Cloud.

Use `streamlit_app.py` as the entrypoint and configure the Groq
credentials through the hosting platform's Secrets settings.

Keep API keys and local database files out of the repository.

For permanent cloud accounts and records, use an external durable
database instead of relying on the hosting server's local SQLite file.

---

## Limitations

- AI features require a valid Groq API key and available models.
- Submitted prompts, PDF excerpts, and images are sent to Groq
  when the corresponding AI feature is used.
- PDF Q&A supports text-based PDFs. Scanned PDFs need OCR first.
- PDF answers use selected excerpts and may miss information
  elsewhere in the document.
- Image text extraction may contain errors and should be checked.
- Invoice comparison supports CSV and Excel files, not PDF invoices.
- Invoice comparison checks item lines; it does not connect to
  AutoCount or perform full accounting reconciliation.
- Login is a learning implementation without password recovery
  or production-grade abuse protection.
- Conversation history is session-based and is not permanently saved.

---

## Project purpose

This project was built to practise Python web development and
demonstrate AI integration, document processing, data visualisation,
authentication, and database operations in one application.
