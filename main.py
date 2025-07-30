import streamlit as st
from parsers.query_parser import parse_user_query
from utils.rag_utils import chunk_text_input, build_or_load_vectorstore, create_qa_chain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

FLIGHT_Q = False # ask question about flight details
VISA_Q = False # ask question about Visa 
STORE_DATA = True # store data from new file/input

if __name__ == "__main__":
    if FLIGHT_Q:
        user_input = input("Enter your prompt:")
        user_input = "Find me a refundable flight from Dubai to Tokyo on August 15th, returning August 30th, \
                    preferably with Star Alliance. I don’t mind a layover in Istanbul."
        parsed_json = parse_user_query(user_input)
        print(parsed_json)
    
    if VISA_Q:
        
        embedding_model = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(
            folder_path="faiss_index", 
            embeddings=embedding_model, 
            allow_dangerous_deserialization=True
        )

        qa_chain = create_qa_chain(vectorstore)  # Already done

        response = qa_chain.run("Do japan citizens need a visa to visit the UAE?")
        print(response)

    if STORE_DATA:
        @st.cache_resource
        def load_visa_qa_chain():
            chunks = chunk_text_input("data/visa_rules.md", input_type="file")
            vectorstore = build_or_load_vectorstore(chunks, index_path="faiss_index")
            return create_qa_chain(vectorstore)

        load_visa_qa_chain()

        embedding_model = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(
            folder_path="faiss_index", 
            embeddings=embedding_model, 
            allow_dangerous_deserialization=True
        )

        retriever = vectorstore.as_retriever()

        # Get all chunks by querying with a wildcard keyword -> or phrases
        docs = retriever.get_relevant_documents("visa")  

        for i, doc in enumerate(docs):
            print(f"Chunk {i + 1}:")
            print(doc.page_content)
            print("-" * 40)
