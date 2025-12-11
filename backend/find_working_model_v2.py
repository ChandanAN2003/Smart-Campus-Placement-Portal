
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
print(f"Key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    genai.configure(api_key=api_key)

# Models seen in the previous list + standard ones
candidates = [
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash",
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash-exp",
    "models/gemini-1.5-flash" 
]

print("Testing models...")
for model_name in candidates:
    print(f"Testing {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"SUCCESS: {model_name}")
        break  # distinct success
    except Exception as e:
        print(f"FAIL {model_name}: {e}")
        time.sleep(1)
