import openai
import os
import subprocess

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_modified_files():
    """Get a list of changed Python files."""
    try:
        files = subprocess.check_output(["git", "diff", "--name-only", "HEAD~1"]).decode().split("\n")
    except subprocess.CalledProcessError:
        print("No previous commit found, running on all files.")
        files = subprocess.check_output(["git", "ls-files"]).decode().split("\n")

    return [file.strip() for file in files if file.endswith(".py")]

def generate_test_code(file_path):
    """Generate test cases for a given file using OpenAI API."""
    with open(file_path, "r") as f:
        code = f.read()

    prompt = f"Write unit tests using pytest for the following Python functions:\n\n{code}"
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    test_code = response['choices'][0]['message']['content']

    test_file_path = f"tests/{os.path.basename(file_path).replace('.py', '_test.py')}"
    os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

    with open(test_file_path, "w") as test_file:
        test_file.write(test_code)

    print(f"AI-generated tests saved to {test_file_path}")

if __name__ == "__main__":
    modified_files = get_modified_files()
    for file in modified_files:
        generate_test_code(file)
