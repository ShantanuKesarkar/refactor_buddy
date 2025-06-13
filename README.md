
# Refactor Buddy 🛠️

**Refactor Buddy** is a Python CLI tool that transforms monolithic Flask applications into modular, production-grade codebases using a Large Language Model (LLM). It breaks down a single large file into a clean directory structure (`routes/`, `models/`, `utils/`) while preserving functionality.

---

## 🚀 Features

- 🔍 **AST-based code analysis**: Uses Python's `ast` module to split code into logical blocks for better context and faster LLM processing.
- 🤖 **LLM-powered refactoring**: Integrates with Mixtral-8x7B-Instruct via Hugging Face to restructure your code.
- 💾 **Automatic backup**: Creates a `.backup` file of your original monolithic source to avoid data loss.
- 💡 **Dry-run mode**: Preview changes without saving any files or modifying your codebase.
- ⚙️ **Hardcoded fallback rules**: If the LLM fails, built-in AST-based logic ensures the code is still grouped reasonably.
- 📁 Modular output: Refactored into a clean structure—`routes/`, `models/`, `utils/`, and an `app.py` entrypoint.

---

## 📂 File Overview

### `refactor_buddy.py`
- This is the **core CLI** script.
- It validates inputs, creates backups, categorizes code via AST, calls the LLM, and saves the refactored result.

### `llm.py`
- Handles **LLM communication** using the Hugging Face `InferenceClient`.
- Sends structured prompts and parses LLM responses into discrete files.

---

## 🧾 Installation

Ensure you have Python 3.8+ and required dependencies:

```bash
pip install transformers huggingface_hub pyyaml
```

---

## 📦 Usage

### 🟢 Basic Refactoring

```bash
python refactor_buddy.py
```

### 🔍 Dry Run (no files written)

```bash
python refactor_buddy.py --dry-run
```

---

## 🖥️ Using as a CLI Tool from CMD (Windows)

To run `refactor-buddy` globally from any directory:

### ✅ Step 1: Create a `.bat` file

1. Open Notepad
2. Paste the following code:

```bat
@echo off
python C:\Users\Shantanu\Desktop\hoopr\refactor_buddy.py %*
```

> Replace the path if your script lives elsewhere.

3. Save the file as `refactor-buddy.bat` inside your project folder or somewhere else.

---

### ✅ Step 2: Add the folder to your system PATH

1. Open **Environment Variables** → Edit the `Path` variable
2. Add:
   ```
   C:\Users\Shantanu\Desktop\hoopr
   ```
3. Save and **restart your CMD window**

---

### ✅ Step 3: Run it from anywhere

Now you can run:

```bash
refactor-buddy --dry-run
```

Or:

```bash
refactor-buddy
```

This will launch the tool and prompt you to select the monolithic file to refactor.

---

## 🧠 About the LLM Prompt

Refactor Buddy uses the Mixtral-8x7B-Instruct model through Hugging Face's Inference API. The prompt sent to the model enforces strict structural refactoring:

- Break monolithic Flask code into modular files
- Separate routes, models, and utility functions
- Define `app = Flask(__name__)` only in `app.py`
- Use `register_routes(app)` in `routes/routes.py`
- Ensure absolute imports and working structure
- Return all files with `# File: path/to/file.py` headers

---

## ⚠️ Why AST-Based Splitting?

Open-source LLMs like Mixtral are powerful but may underperform compared to models like GPT-4 on long or cluttered inputs. To improve performance:
- We **pre-process** code using Python's `ast` module to break it into logical categories
- These smaller chunks are fed to the LLM for better accuracy and speed

If the LLM fails, the tool uses **hardcoded AST rules** to group code effectively as a fallback.

---

## 📁 Output Structure Example

```
Desktop/
└── refactored_code/
    ├── app.py
    ├── models/
    │   ├── __init__.py
    │   └── user.py
    ├── routes/
    │   ├── __init__.py
    │   └── routes.py
    ├── utils/
    │   ├── __init__.py
    │   └── helpers.py
```

---
## 🙋 Support or Questions?

Feel free to open an issue or suggest improvements!


Added a temporary key for just test use case in the .env file
