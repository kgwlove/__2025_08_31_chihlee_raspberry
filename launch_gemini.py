import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

print("🤖 Gemini Chat Session Started!")
print("Type 'quit' or 'exit' to end the session.\n")

while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        response = model.generate_content(user_input)
        print(f"Gemini: {response.text}\n")
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"Error: {e}\n")
