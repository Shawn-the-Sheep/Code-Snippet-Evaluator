# LLM-Assisted Python Code Review Tool

This script reviews short Python code snippets using OpenAI's GPT-4o model via the OpenAI API. It analyzes each snippet, provides review feedback, and assigns a quality rating (`Good`, `Needs Improvement`, or `Buggy`).

---

## 🚀 What It Does

- Loads 3–5 Python code snippets from a JSON file.
- Sends each snippet to an LLM (GPT-4o) with an appropriate review prompt.
- Logs the LLM’s responses.
- Assigns a quality flag to each snippet.
- Saves the results to a new output JSON file.

---

## 🛠️ Setup Instructions

### 1. Clone the Project or Download the Files

Make sure you have Python 3.7+ installed.

### 2. Install Required Packages

```bash
pip install openai python-dotenv
```
### 3. Set Up Your OpenAI API Key

🔐 This project requires your own OpenAI API Key

1. Create a .env file at the root of the project (in the same folder as code_review.py)

2. Add the following line to the .env file

OPENAI_API_KEY="your-secret-api-key-here"

If you don't have an API key yet, you can get one by creating an account at https://platform.openai.com.

## 📥 Input File Format (python_snippets.json)

Your input file must be a JSON array of snippet objects.

Each object must contain:

id: a unique identifier for the snippet

code: the Python code snippet as a string

Example:

```json
[
  {
    "id": 1,
    "code": "def add(a, b):\n    return a + b"
  },
  {
    "id": 2,
    "code": "for i in range(5):\n    print(i)"
  }
]
```
## 📥 Output File Format (reviewed_snippets.json)

After running the script, the results are saved to reviewed_snippets.json.

Each object includes:

id: the original snippet ID

code: the original code

GPT-4o Response: the full review message from GPT

Quality Flag: one of Good, Needs Improvement, or Buggy

Example:

```json
[
  {
    "id": 1,
    "code": "def add(a, b):\n    return a + b",
    "GPT-4o Response": "This is a simple, clean, and correct function...",
    "Quality Flag": "Good"
  }
]
```

## ▶️ How to Run the Script

After setting up your .env and input file:

```bash
python code_review.py
```

The output will be saved to reviewed_snippets.json.
