import openai
import os
import subprocess

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_changed_code():
    """Retrieve only the changed lines in main.py using Git."""
    try:
        # Get the changed lines in main.py
        diff_output = subprocess.run(
            ["git", "diff", "-U0", "HEAD~1", "--", "main.py"], 
            capture_output=True, text=True, check=True
        ).stdout

        changed_lines = []
        for line in diff_output.split("\n"):
            if line.startswith("+") and not line.startswith("+++"):  # Ignore metadata lines
                changed_lines.append(line[1:])  # Remove "+" sign

        return "\n".join(changed_lines)

    except subprocess.CalledProcessError:
        print("Error retrieving git diff. Ensure you're running this inside a git repository.")
        return ""

def generate_test_code(changed_code):
    """Generate AI-powered tests only for changed code in main.py."""
    if not changed_code.strip():
        print("No changes detected in main.py. Skipping test generation.")
        return

    prompt = f"Write unit tests using pytest only for the following changed Python code:\n\n{changed_code}"

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
    changed_code = get_changed_code()
    generate_test_code(changed_code)
