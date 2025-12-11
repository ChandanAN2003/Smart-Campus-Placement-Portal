
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("No GEMINI_API_KEY found")
else:
    genai.configure(api_key=api_key)
    print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
    
    try:
        models = genai.list_models()
        generation_models = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                generation_models.append(m.name)
        
        print(f"Found {len(generation_models)} generation models.")
        
        # Priority list to test
        priority_models = [
            'models/gemini-1.5-flash',
            'models/gemini-2.0-flash-exp',
            'models/gemini-2.0-flash',
            'models/gemini-1.5-pro',
            'models/gemini-pro'
        ]
        
        # Add others from discovery if not in priority
        for m in generation_models:
            if m not in priority_models:
                priority_models.append(m)

        for model_name in priority_models:
            if model_name not in generation_models:
                continue

            print(f"\nTesting model: {model_name}")
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say 'OK'")
                print(f"SUCCESS with {model_name}: {response.text}")
                # If success, we found our winner
                with open('working_model.txt', 'w') as f:
                    f.write(model_name)
                    break 
            except Exception as e:
                print(f"FAILED with {model_name}: {e}")
                time.sleep(1) # mild backoff

    except Exception as e:
        print(f"Error listing/testing models: {e}")
