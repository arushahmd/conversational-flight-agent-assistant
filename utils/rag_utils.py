import os
from typing import Literal, Optional, Union
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA  

def chunk_text_input(
                        source: Union[str, list[Document]], 
                        input_type: Literal["file", "text"]
                    ) -> list[Document]:
    """
        Create chunks of the text at hand
    """
    if input_type == "file":
        loader = TextLoader(source)
        documents = loader.load()
    elif input_type == "text":
        documents = [Document(page_content=source)] # type: ignore 
    else:
        raise ValueError("input_type must be 'file' or 'text'")

    # splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150) # i'm overlapping as data is related
    return splitter.split_documents(documents)


def build_or_load_vectorstore(
                                chunks: list[Document], 
                                embedding_model=None,
                                index_path: Optional[str] = None
                            ) -> FAISS:
    """
        Load or build the vector store if not exist
    """
    embedding_model = embedding_model or OpenAIEmbeddings()

    if index_path and os.path.exists(index_path):
        return FAISS.load_local(index_path, embedding_model)
    
    vectorstore = FAISS.from_documents(chunks, embedding_model)

    if index_path:
        vectorstore.save_local(index_path)
    
    return vectorstore


def create_qa_chain(
                        vectorstore: FAISS, 
                        model_name: str = "gpt-3.5-turbo"
                    ) -> RetrievalQA:
    """
        Q/A chain to retrieve data from the database
    """
    llm = ChatOpenAI(model=model_name)
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
