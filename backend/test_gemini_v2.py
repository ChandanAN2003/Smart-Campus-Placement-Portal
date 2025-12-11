import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    
    print("\n--- Testing 2.5-flash with System Instructions & Config ---")
    try:
        system_instruction = "You are a helpful AI."
        model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_instruction)
        
        prompt = "Generate 2 fake mock test questions in JSON format."
        
        response = model.generate_content(
            prompt, 
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000,
                temperature=0.7
            )
        )
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Full Config Failed: {e}")

    print("\n--- Testing 2.5-flash RAW ---")
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content("Hello")
        print(f"Raw Success! Response: {response.text}")
    except Exception as e:
        print(f"Raw Failed: {e}")
