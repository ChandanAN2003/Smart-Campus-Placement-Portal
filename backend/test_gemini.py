import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key present: {bool(api_key)}")

if api_key:
    genai.configure(api_key=api_key)
    
    models_to_test = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-pro"]
    
    for model_name in models_to_test:
        print(f"\n--- Testing {model_name} ---")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello, are you working?")
            print(f"Success! Response: {response.text}")
        except Exception as e:
            print(f"Failed: {e}")
