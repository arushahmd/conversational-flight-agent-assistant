import streamlit as st
import pandas as pd
from parsers.query_parser import parse_user_query

from flight_search.search import get_available_routes
from utils.rag_utils import create_qa_chain

st.set_page_config(page_title="✈️ Flight Booking Assistant", page_icon="✈️", layout="centered") #Title of the page

with st.sidebar:
    st.sidebar.title("✈️ FlightQuery")

query_type = st.sidebar.radio(
    "Choose the type of query:",
    ["Flight Info", "Visa Info"],
    help="Select whether you want to search flights or ask about visa policies."
)

with st.sidebar.expander("💡 What can I ask?"):
    st.markdown("### ✈️ Flight Info Examples")
    st.markdown("- Find me a refundable flight from Dubai to Tokyo on August 15th, returning August 30th, preferably with Star Alliance. I don’t mind a layover in Istanbul.")
    st.markdown("- Can you find me a refundable flight from Lahore to London on August 20th, coming back by September 5th? Preferably with Oneworld alliance.")
    
    st.markdown("### 🛂 Visa Info Examples")
    st.markdown("- Do I need a visa to go from UAE to Japan?")
    st.markdown("- Visa policy for Pakistani citizens visiting the UK")

st.markdown("<h2 style='text-align: center;'>Flight Booking Assistant</h2>", unsafe_allow_html=True)
st.markdown("#### Ask your question below:")

placeholder_text = (
    "e.g., Book a flight from Dubai to Tokyo on August 15"
    if query_type == "Flight Info"
    else "e.g., Do I need a visa to travel from UAE to Japan?"
)

if query_type == "Flight Info":
    available_routes = get_available_routes()
    with st.expander("✈️ Available Routes"):
        st.markdown(", ".join(available_routes[:10]))

user_query = st.text_input("Your Query", placeholder=placeholder_text) # Get user input

# Main loop that triggers on button click
if st.button("Submit"):
    if user_query.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        st.info("Processing your request...")

        if query_type == "Flight Info":
            flight_results = parse_user_query(user_query) 
            if flight_results == []:
                st.warning("No matching flights found with the exact origin and destination.")
            else:
                st.success("Flight information found:") 
                df = pd.DataFrame(flight_results)
                st.dataframe(df)

                with st.expander("🔍 See Raw Json"):
                    st.json(flight_results)
        
        elif query_type == "Visa Info":
            st.success("Visa information:")
            response = parse_user_query(user_query)

            if isinstance(response, dict):
                refined = response.get("llm_refined_answer")
                
                if hasattr(refined, "content"): 
                    refined_answer = refined.content
                else:
                    refined_answer = refined or "No refined answer found."

                st.markdown("### ✈️ Visa Information")
                st.success(refined_answer)

                with st.expander("🔍 See Retrieved Document Info (RAG DB)"):
                    st.markdown(response.get("raw_db_answer", "No info found."))

            else:
                st.warning("Sorry, I couldn't understand your query or no relevant data was found.")    