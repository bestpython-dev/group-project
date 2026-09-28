# Student Management System

A polished Streamlit registry for a seven-person academic group project. Staff can add, view, edit and delete student records; every field is checked with regular expressions; every record is saved to a CSV file; failures never crash the app; Gemini can answer class questions; Gmail SMTP sends a grade report.

The work is split exactly as the proposal required: **one folder per teammate**.

---

## Run it

```bash
cd student-management-system
py -3 -m pip install -r requirements.txt
py -3 -m streamlit run app.py
```

On Windows you can also double-click `run.bat`.

Optional keys go in a `.env` file (copy `.env.example`):

| Variable | Purpose |
| --- | --- |
| `GEMINI_API_KEY` | Live Gemini answers and written summaries |
| `GMAIL_ADDRESS` | Sender for grade reports |
| `GMAIL_APP_PASSWORD` | Gmail **app password**, not the normal login |

Without those keys the rest of the system still runs. The AI page answers from the live register, and the email page still shows a full report preview.

---

## Who built what

| Member | Folder | Responsibility | Proposed branch |
| --- | --- | --- | --- |
| Asher Gbolahan | `Asher_Gbolahan/` | `Student` and `StudentManager` (OOP) | `Asher_Gbolahan` |
| Grace Ukpai Akpu | `Grace_Ukpai_Akpu/` | `save_to_file()` / `load_from_file()` | `Grace_Ukpai_Akpu` |
| Great Joseph | `Great_Joseph/` | Regex validation | `Great_Joseph` |
| Oluwakorede Olawoye | `Oluwakorede_Olawoye/` | Add Student, View Students, dashboard | `Oluwakorede_Olawoye` |
| Abubakar Nuradden | `Abubakar_Nuradden/` | Edit Student, Delete Student | `Abubakar_Nuradden` |
| Ismail Muhammed | `Ismail_Muhammed/` | Custom exceptions + `safe_action()` | `Ismail_Muhammed` |
| Aliyu Bappa | `Aliyu_Bappa/` | Gemini, Gmail SMTP, this README | `Aliyu_Bappa` |

`app.py` is the shared shell. It only composes the folders above.

---

## Required topics

**OOP** — `Student` keeps fields private and exposes getters/setters, letter grades, and standing. `StudentManager` is the only class that adds, finds, edits, deletes, and asks the file layer to persist.

**File handling** — Python’s built-in `csv` module reads and writes `data/students.csv`. Every successful add, edit or delete rewrites the file immediately.

**Regular expressions** — `Great_Joseph/validate.py` checks student ID, name, email, phone, course and grade. Add and Edit both call the same functions.

**Exception handling** — File I/O, Gemini HTTP calls, and SMTP login/send all go through `safe_action()`. Expected problems raise `DuplicateStudentError`, `StudentNotFoundError`, `ValidationError`, `FileOperationError`, `AIServiceError` or `EmailServiceError`, and Streamlit shows a sentence instead of a traceback.

**GUI** — Streamlit sidebar navigation, dashboard metrics, searchable register, forms, confirmation on delete.

**Gemini AI** — Ask a class question or generate a one-paragraph student summary via the Gemini REST API.

**External API** — Grade reports are sent with Python’s built-in `smtplib` against `smtp.gmail.com`.

---

## Project layout

```
app.py
requirements.txt
data/students.csv
assets/styles.css
Asher_Gbolahan/
Grace_Ukpai_Akpu/
Great_Joseph/
Oluwakorede_Olawoye/
Abubakar_Nuradden/
Ismail_Muhammed/
Aliyu_Bappa/
```

---

## Git workflow (as proposed)

```bash
git checkout -b Asher_Gbolahan
git checkout -b Grace_Ukpai_Akpu
git checkout -b Great_Joseph
git checkout -b Oluwakorede_Olawoye
git checkout -b Abubakar_Nuradden
git checkout -b Ismail_Muhammed
git checkout -b Aliyu_Bappa
```

Merge into `main` through pull requests, one branch per person.

---

*Team lead: Asher Gbolahan. Built to match the group project proposal — GUI, OOP, file handling, exceptions, regex, Gemini, and an external email service.*


## Interface refresh and OpenAI assistant
The interface uses a bright blue and teal CampusHub theme. Team ownership folders are preserved.
Set `OPENAI_API_KEY` in the local, Git-ignored `.env` file and select OpenAI on the AI Assistant page.
`OPENAI_MODEL` defaults to `gpt-4.1-mini` and can be changed to a model available to your API project.
Never share the key in chat or commit `.env`. No key is bundled with the project.
The assistant sends academic context only when you submit a question or generate a summary.
Local insights remain available without credentials. Gemini remains selectable.
API documentation: https://developers.openai.com/api/docs/quickstart
CSV writes now use atomic replacement; failed writes reload the saved records.
