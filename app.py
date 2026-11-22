
import streamlit as st
from travel_ai import generate_itinerary
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .main {
        background-color: #ffffff;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: bold;
    }

    .travel-title {
        text-align: center;
        color: #1E3A5F;
        font-size: 35px;
        font-weight: bold;
    }

    .travel-subtitle {
        text-align: center;
        color: #666666;
        font-size: 16px;
    }

    .success-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #e8f5e9;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="travel-title">🌍 AI Travel Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="travel-subtitle">'
    'Plan your perfect trip with the power of AI!'
    '</div>',
    unsafe_allow_html=True
)

st.write("")

st.markdown("""
Enter your travel preferences below.
Our AI will create a personalized travel itinerary
based on your destination, interests and budget.
""")

st.divider()

# --------------------------------------------------
# TRAVEL PREFERENCES
# --------------------------------------------------

st.header("🌍 Your Travel Preferences")

# Destination
destination = st.text_input(
    "Where do you want to travel?",
    placeholder="Example: Goa, Manali, Jaipur",
    value="Goa"
)

# Days and Budget
col1, col2 = st.columns(2)

with col1:
    days = st.number_input(
        "Number of travel days",
        min_value=1,
        max_value=30,
        value=3,
        step=1
    )

with col2:
    budget = st.number_input(
        "Your total budget (₹)",
        min_value=1000,
        max_value=10000000,
        value=15000,
        step=1000
    )

# Interests
interest_options = [
    "Sightseeing",
    "Beaches",
    "Nature",
    "Adventure",
    "Food",
    "Shopping",
    "History",
    "Culture",
    "Nightlife",
    "Photography",
    "Wildlife",
    "Spirituality"
]

interests = st.multiselect(
    "Select your travel interests",
    options=interest_options,
    default=["Sightseeing", "Beaches", "Nature"]
)

# Number of travelers
travelers = st.number_input(
    "Number of travelers",
    min_value=1,
    max_value=20,
    value=2,
    step=1
)

# Travel month
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

current_month = datetime.now().month - 1

travel_month = st.selectbox(
    "Select your travel month",
    options=months,
    index=current_month
)

st.write("")

# --------------------------------------------------
# GENERATE TRAVEL PLAN
# --------------------------------------------------

if st.button("✨ Generate My Travel Plan", type="primary"):

    if not destination.strip():
        st.error("Please enter your travel destination.")

    elif not interests:
        st.error("Please select at least one travel interest.")

    elif days < 1 or travelers < 1 or budget <= 0:
        st.error("Please enter valid travel details.")

    else:

        # Convert interests into a readable string
        selected_interests = ", ".join(interests)

        try:
            with st.spinner(
                "🌍 Your AI Travel Planner is preparing your trip..."
            ):

                result = generate_itinerary(
                    destination=destination.strip(),
                    days=int(days),
                    budget=int(budget),
                    interests=selected_interests,
                    travelers=int(travelers),
                    travel_month=travel_month
                )

            if result:

                st.success(
                    "🎉 Your personalized travel itinerary is ready!"
                )

                st.divider()

                # Display generated itinerary
                st.header(
                    f"✈️ Your AI Travel Plan for {destination.title()}"
                )

                st.markdown(result)

                st.divider()

                # Download itinerary
                st.download_button(
                    label="📥 Download Your Travel Plan",
                    data=result,
                    file_name=f"{destination.lower().replace(' ', '_')}_travel_plan.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                st.balloons()

            else:
                st.error(
                    "The AI returned an empty response. Please try again."
                )

        except Exception as e:
            st.error(
                f"Unable to generate your travel plan: {str(e)}"
            )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<div style='text-align:center; color:gray;'>"
    "🌍 AI Travel Planner | Powered by Groq AI"
    "<br>Plan smarter. Travel better."
    "</div>",
    unsafe_allow_html=True
)
