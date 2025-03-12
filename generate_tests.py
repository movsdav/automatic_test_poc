import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_test_code():
    """Generate test cases using OpenAI."""
    with open("app.py", "r") as f:
        code = f.read()

    prompt = f"Write unit tests using pytest for the following Python functions:\n\n{code}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    test_code = response['choices'][0]['message']['content']

    with open("ai_generated_tests.py", "w") as test_file:
        test_file.write(test_code)

    print("AI-generated tests saved to ai_generated_tests.py")

if __name__ == "__main__":
    generate_test_code()
