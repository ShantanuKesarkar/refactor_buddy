import os
import re
from huggingface_hub import InferenceClient
from transformers import AutoTokenizer
from dotenv import load_dotenv


load_dotenv()
token = os.getenv("token")

# HF API setup (Mixtral)
client = InferenceClient(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    token=token,
)

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x7B-Instruct-v0.1")

def split_into_chunks(text, max_tokens=32000):
    lines = text.split("\n")
    chunks = []
    current_chunk = []
    current_tokens = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        tokenized_line = tokenizer.tokenize(line)
        line_tokens = len(tokenized_line)

        if current_tokens + line_tokens > max_tokens - 500:  # leave buffer for prompt
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_tokens = 0

        current_chunk.append(line)
        current_tokens += line_tokens

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks

def send_chunk_to_model(chunk):
    prompt = (
        "You are a senior Python engineer. Refactor the following monolithic Flask application into a modular, production-grade project.\n\n"
        "Strictly follow these rules:\n"
        "- Separate logic into: routes/, models/, utils/\n"
        "- Put route handlers inside routes/routes.py\n"
        "- Wrap all route definitions in a function: register_routes(app)\n"
        "- Define `app = Flask(__name__)` **only** in app.py\n"
        "- app.py **must call** register_routes(app)\n"
        "- In routes/__init__.py add: `from routes.routes import register_routes`\n"
        "- Use **absolute imports** like `from routes.routes import register_routes`, not relative ones\n"
        "- Add all required imports in each file (e.g., from flask import request, jsonify)\n"
        "- Add empty `__init__.py` in each folder (routes, models, utils)\n"
        "- Ensure the final structure runs out-of-the-box with `python app.py`\n"
        "- Output each file using `# File: path/to/file.py` format\n\n"
        f"Here is the code to refactor:\n{chunk}"
    )

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            max_tokens=2048,
            temperature=0.7,
        )
        try:
            return response.choices[0].message.content
        except Exception as inner_e:
            raise ValueError(f"Invalid LLM response: {inner_e}\nRaw response: {response}")
    except Exception as e:
        raise ValueError(f"LLM call failed: {e}")

def parse_response_into_files(response_text):
    if '# File:' not in response_text:
        raise ValueError("LLM response did not contain any file headers.")
    
    file_blocks = re.split(r'# File: (.+)', response_text)
    files = {}
    for i in range(1, len(file_blocks), 2):
        path = file_blocks[i].strip()
        content = file_blocks[i + 1].strip()
        if path in files:
            print(f"Warning: Duplicate file path {path}, overwriting.")
        files[path] = content
    return files

def analyze_and_refactor(categorized_code):
    code_string = "\n".join([f"# --- {key} ---\n" + "\n".join(value) for key, value in categorized_code.items()])
    chunks = split_into_chunks(code_string)

    refactored_output = {}
    for i, chunk in enumerate(chunks):
        print(f"Sending chunk {i + 1}/{len(chunks)} to Mixtral...")
        try:
            llm_response = send_chunk_to_model(chunk)
            files = parse_response_into_files(llm_response)
            refactored_output.update(files)
        except Exception as e:
            print(f"Error processing chunk {i + 1}: {e}")
            return None

    return refactored_output
