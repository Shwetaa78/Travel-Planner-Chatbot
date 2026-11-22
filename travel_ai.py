
import os
from dotenv import load_dotenv
from groq import Groq, RateLimitError, AuthenticationError, APIConnectionError, APIStatusError

# Load environment variables
load_dotenv()

# Read Groq configuration
API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

# Check API key
if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )

# Initialize Groq client
client = Groq(api_key=API_KEY)


def generate_itinerary(
    destination,
    days,
    budget,
    interests,
    travelers,
    travel_month
):
    """
    Generate a personalized travel itinerary using Groq AI.
    """

    # Create the travel planning prompt
    prompt = f"""
You are an expert AI Travel Planner.

Your task is to create a personalized, practical
and budget-conscious travel itinerary.

USER TRAVEL DETAILS:

Destination: {destination}
Number of days: {days}
Total budget: INR {budget}
Interests: {interests}
Number of travelers: {travelers}
Travel month: {travel_month}

YOUR TASK:

Create a detailed travel plan using the information above.

FOLLOW THESE INSTRUCTIONS:

1. Create a separate itinerary for every travel day.

2. Divide every day into:
   - Morning
   - Afternoon
   - Evening

3. Suggest popular attractions and activities
   suitable for the destination.

4. Prioritize the user's selected interests.

5. Include approximate accommodation expenses.

6. Include approximate food expenses.

7. Include local transportation expenses.

8. Include sightseeing and activity expenses.

9. Give a day-wise estimated expense breakdown.

10. Calculate the approximate total trip cost.

11. Compare the total estimated cost with
    the user's available budget.

12. Suggest ways to save money if the budget
    is insufficient.

13. Include useful travel tips.

OUTPUT FORMAT:

# AI Travel Plan for {destination}

## 1. Trip Overview
- Destination
- Duration
- Number of travelers
- Total budget
- Travel month

## 2. Day-wise Travel Itinerary

For every day, include:

### Day 1
Morning:
Afternoon:
Evening:
Estimated daily expenses:

Continue for all requested days.

## 3. Estimated Budget Breakdown

Accommodation:
Food:
Transportation:
Activities:
Miscellaneous:

## 4. Total Estimated Cost

## 5. Budget Comparison

State whether the trip is within budget
or exceeds the available budget.

## 6. Travel Tips

Provide useful and practical suggestions.

IMPORTANT RULES:

- Use Indian Rupees (INR).
- Keep the itinerary realistic.
- Consider the number of travelers.
- Make cost estimates consistent with the total budget.
- Do not claim prices are live or verified.
- Do not claim that hotels or tickets are booked.
- Clearly mention that all prices are approximate.
- Do not invent confirmed availability.
- If information is uncertain, state that clearly.
"""

    try:

        # Send prompt to Groq
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional AI travel planner. "
                        "Give accurate, structured, helpful and "
                        "budget-conscious travel recommendations."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=5000
        )

        # Extract AI response
        itinerary = response.choices[0].message.content

        if not itinerary:
            raise RuntimeError("Groq returned an empty response.")

        return itinerary

    except AuthenticationError as e:
        raise RuntimeError(
            "Groq authentication failed. Check your GROQ_API_KEY "
            "in the .env file."
        ) from e

    except RateLimitError as e:
        raise RuntimeError(
            "Groq API rate limit or quota exceeded. "
            "Check your Groq Console usage and limits."
        ) from e

    except APIConnectionError as e:
        raise RuntimeError(
            "Unable to connect to Groq. Check your internet connection."
        ) from e

    except APIStatusError as e:
        raise RuntimeError(
            f"Groq API error: {e.status_code}. {e.message}"
        ) from e

    except Exception as e:
        raise RuntimeError(
            f"Unable to generate itinerary: {str(e)}"
        ) from e
