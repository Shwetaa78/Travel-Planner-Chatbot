from travel_ai import generate_itinerary

try:
    result = generate_itinerary(
        destination="Goa",
        days=3,
        budget=15000,
        interests="Beaches, food, sightseeing",
        travelers=2,
        travel_month="December"
    )

    print("\n===== YOUR AI TRAVEL PLAN =====\n")
    print(result)

except Exception as e:
    print("ERROR:", e)