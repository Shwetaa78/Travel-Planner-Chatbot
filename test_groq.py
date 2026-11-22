
print("TEST SCRIPT STARTED")

import os
from dotenv import load_dotenv
from groq import Groq

print("Loading environment variables...")

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY not found in .env")

else:
    print("API key found!")

    client = Groq(api_key=api_key)

    print("Connecting to Groq...")

    try:
        response = client.chat.completions.create(
            model=os.getenv(
                "GROQ_MODEL",
                "openai/gpt-oss-20b"
            ),
            messages=[
                {
                    "role": "user",
                    "content": "Say hello in one short sentence."
                }
            ],
            max_completion_tokens=200
        )

        print("\nSUCCESS! Groq is connected.")
        print("AI Response:")
        print(response.choices[0].message.content)

    except Exception as e:
        print("\nERROR:")
        print(type(e).__name__)
        print(str(e))
