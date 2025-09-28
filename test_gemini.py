import google.generativeai as genai
import os

# Configure with your API key from environment variable
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not found")
    exit(1)

genai.configure(api_key=api_key)

# List available models
print("Available models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")

# Use the current Gemini model name
model = genai.GenerativeModel('gemini-1.5-flash')

# Test with a simple prompt
try:
    print("\nTesting Gemini connection...")
    response = model.generate_content("Say hello and confirm that Gemini is working!")
    print("✅ Success! Gemini response:")
    print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")
