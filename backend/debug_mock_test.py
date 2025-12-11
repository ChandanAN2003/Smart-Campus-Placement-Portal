from gemini_ai import generate_mock_test
import sys
import os

# Mock the environment variable if needed, though .env should be loaded by gemini_ai
from dotenv import load_dotenv
load_dotenv()

print("Testing generate_mock_test...")
try:
    questions = generate_mock_test("Python Developer", "Medium")
    print(f"Got {len(questions)} questions.")
    if len(questions) > 0:
        print(f"Sample: {questions[0]}")
    else:
        print("Got empty list.")
except Exception as e:
    print(f"Error calling function: {e}")
