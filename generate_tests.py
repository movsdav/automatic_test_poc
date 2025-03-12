import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_main_py_content():
    """Reads the full content of main.py."""
    try:
        with open("main.py", "r") as f:
            return f.read()
    except FileNotFoundError:
        print("Error: main.py not found.")
        return ""

def generate_test_code():
    """Generates AI-powered tests for main.py."""
    code = get_main_py_content()
    
    if not code.strip():
        print("Error: main.py is empty. Skipping test generation.")
        return

    prompt = f"Write unit tests using pytest for the following Python functions:\n\n{code}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that generates Python unit tests."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    test_code = response["choices"][0]["message"]["content"]

    with open("ai_generated_tests.py", "w") as test_file:
        test_file.write(test_code)

    print("✅ AI-generated tests saved to ai_generated_tests.py")

if __name__ == "__main__":
    generate_test_code()
