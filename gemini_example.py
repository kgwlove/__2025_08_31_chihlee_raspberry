import os
import google.generativeai as genai

# Configure the API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("Please set your GOOGLE_API_KEY environment variable")
    print("Get your API key from: https://makersuite.google.com/app/apikey")
    exit(1)

genai.configure(api_key=api_key)

# Create a model instance
model = genai.GenerativeModel('gemini-pro')

# Example usage
def chat_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Interactive chat
    print("Gemini Chat (type 'quit' to exit)")
    print("-" * 40)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        response = chat_with_gemini(user_input)
        print(f"Gemini: {response}")
