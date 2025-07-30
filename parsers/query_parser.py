import os
from typing import List
from dotenv import load_dotenv

from flight_search.search import load_flights, match_flights
from utils.rag_utils import create_qa_chain
load_dotenv()

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, RootModel
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

# Output Schema -> in json format.
class FlightSearchQuery(BaseModel):
    origin: str = Field("", description="City the user is departing from")
    destination: str = Field("", description="City the user wants to travel to")
    departure_date: str = Field("", description="When the user wants to leave")
    return_date: str = Field("", description="Return date if round-trip")
    alliance: str = Field("", description="Preferred airline alliance if specified")
    refundable: bool = Field(False, description="Does the user want a refundable ticket?")
    avoid_overnight_layovers: bool = Field(False, description="Avoid overnight layovers")
    layovers: str = Field("", description="List of layovers")


class FlightSearchList(RootModel[List[FlightSearchQuery]]):
    pass


parser = PydanticOutputParser(pydantic_object=FlightSearchList)

flight_template = """
                    You are an AI assistant helping users search for flights.

                    Your task is to extract structured flight search parameters from the user's query. The user may request information for one or more flights.

                    -  Output must always be a JSON **list of objects**, even if only one flight is mentioned.
                    - Each JSON object must match the format below exactly, using **all fields** from the format instructions.
                    - If a field is not mentioned or implied in the user query, use a **default empty value**:
                        - Use `""` for strings
                        - Use `false` for booleans
                        - Use `[]` for lists
                        - Use `0` for numbers if appropriate

                    ---

                    User Query:
                    {query}

                    Format Instructions:
                    {format_instructions}

                    Notes:
                    - The user may describe multiple flights in one sentence, like:
                    `"Search Dubai to Tokyo, Dubai to Frankfurt, Lahore, Turkey to Tokyo"`
                    - Extract each pair as a separate object.
                    - Normalize city names (trim spaces, use standard casing).
                    - Do **not** guess values that are not present — just leave them empty as instructed.

                    Output:
                    Return a valid JSON list of all flight search objects.
"""

prompt = PromptTemplate(
    template=flight_template,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

llm = ChatOpenAI(model="gpt-3.5-turbo")

llm_chain = prompt | llm | parser

# Keyword matchers
VISA_KEYWORDS = ["visa", "passport", "entry", "immigration", "tourist"]
FLIGHT_KEYWORDS = ["book", "flight", "round-trip", "ticket", "one-way", "layover", "departure", "airline"]

def classify_query(query: str) -> str:
    """
        Classifies the query as visa or flight based on some keywords.
    """
    query_lower = query.lower()
    if any(kw in query_lower for kw in VISA_KEYWORDS):
        return "visa"
    elif any(kw in query_lower for kw in FLIGHT_KEYWORDS):
        return "flight"
    else:
        return "unknown"

def get_flight_info(query: str): # TODO: place the function in correct module
    """
        Returns flight json and matched flights, top-3 flight details are returned for now.
    """
    parsed = llm_chain.invoke(query)
    queries = [q.dict() for q in parsed.root]
    flights = load_flights()
    results = match_flights(queries, flights)

    return results or [] # "No matching flights found."

def get_visa_info(query: str): # TODO: place the function in correct module
    """
    Retrieves visa/refund info using FAISS RAG, then passes it to LLM for final refinement.
    Returns both raw and LLM-refined answers.
    """

    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(
        folder_path="faiss_index",
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )

   
    qa_chain = create_qa_chain(vectorstore)
    db_answer = qa_chain.run(query)

    
    visa_info_prompt = PromptTemplate.from_template(
        """
        You are a travel assistant. Below is an answer fetched from a document database.
        Please rephrase it clearly and concisely for the user.

        Question: {query}
        Retrieved Info: {context}

        Final Answer:
        """
    )

    chat_llm=ChatOpenAI(temperature=0) # I want authentic answer no creativity


    refinement_chain = visa_info_prompt | chat_llm 

    llm_response = refinement_chain.invoke({
        "query": query,
        "context": db_answer
    })

    return {
        "raw_db_answer": db_answer,
        "llm_refined_answer": llm_response
    }

def parse_user_query(query: str): # TODO: handle cases when None is returned as result
    """
        Parse the query and call the relevant chain or function to get output.
    """
    intent = classify_query(query)
    if intent == "flight":
        print("Flight Query")
        result = get_flight_info(query)      
        return result 
    
    elif intent == "visa":
        print("Visa Query")
        result = get_visa_info(query)
        return result
    else:
        print("Couldn't classify query type.")
        return None