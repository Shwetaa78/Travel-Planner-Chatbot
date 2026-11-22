
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")

print("Connecting to Gemini...")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model=model,
        contents="Say hello in one short sentence."
    )

    print("\nGemini response:")
    print(response.text)

except Exception as e:
    print("\nGemini connection failed:")
    print(type(e).__name__, str(e))