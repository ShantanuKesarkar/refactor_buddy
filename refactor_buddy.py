import os
import ast
import argparse
from llm import analyze_and_refactor

def validate_file(file_path):
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")
    if not file_path.endswith(('.py', '.js')):
        raise ValueError("Only .py and .js files are supported.")

def create_backup(file_path):
    backup_path = f"{file_path}.backup"
    with open(file_path, 'r') as original, open(backup_path, 'w') as backup:
        backup.write(original.read())
    print(f"Backup created at: {backup_path}")

def categorize_code_ast(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    blocks = {
        "Imports": [],
        "Initialization": [],
        "Models": [],
        "Utils": [],
        "Routes": [],
        "Main": [],
        "Others": []
    }

    seen_lines = set()

    for node in ast.walk(tree):
        line = ast.unparse(node)
        if line in seen_lines:
            continue
        seen_lines.add(line)

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            blocks["Imports"].append(line)
        elif isinstance(node, ast.Assign):
            targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if any(name in targets for name in ["app", "server", "application"]):
                blocks["Initialization"].append(line)
        elif isinstance(node, ast.ClassDef):
            blocks["Models"].append(line)
        elif isinstance(node, ast.FunctionDef):
            if any(isinstance(d, ast.Attribute) and d.attr == "route" for d in node.decorator_list):
                blocks["Routes"].append(line)
            else:
                blocks["Utils"].append(line)
        elif isinstance(node, ast.If):
            if isinstance(node.test, ast.Compare) and getattr(node.test.left, 'id', None) == "__name__":
                blocks["Main"].append(line)
        elif isinstance(node, (ast.Expr, ast.Str, ast.Call)):
            blocks["Others"].append(line)

    return blocks

def save_refactored_output(refactored_code, output_dir=os.path.join(os.path.expanduser("~"), "Desktop", "refactored_code")):
    entrypoints = []
    for relative_path, content in refactored_code.items():
        file_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(content)
        if "if __name__ == '__main__':" in content:
            entrypoints.append(file_path)
    print(f"\n✅ Refactored code saved to: '{output_dir}'")

    # Optionally test the main file
    if entrypoints:
        print("\n🚀 Testing main entrypoint...")
        try:
            os.system(f"python {entrypoints[0]}")
        except Exception as e:
            print(f"❌ Failed to run the app: {e}")

def main():
    print("👋 Welcome to your Refactoring Buddy!")
    file_path = input("📂 Please enter the path to your monolithic Python or JavaScript file: ").strip()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the tool without saving or executing the refactored code"
    )
    args = parser.parse_args()

    try:
        validate_file(file_path)
        create_backup(file_path)

        print("🔍 Categorizing code...")
        blocks = categorize_code_ast(file_path)

        print("🧠 Sending code to LLM for refactoring...")
        refactored_code = analyze_and_refactor(blocks)

        if refactored_code:
            if args.dry_run:
                print("\n🧪 Dry Run: Refactored code would include the following files:")
                for path in refactored_code:
                    print(f" - {path}")
                # Optional: preview one file
                preview_path = list(refactored_code.keys())[0]
                print(f"\n📄 Preview of {preview_path}:\n")
                print(refactored_code[preview_path][:500] + "\n...")
            else:
                save_refactored_output(refactored_code)
        else:
            print("❌ Refactoring failed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
