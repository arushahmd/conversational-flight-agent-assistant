# ✈️ Conversational Travel Assistant

[![Python](https://img.shields.io/badge/.py-Python-blue?logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/.-LangChain-green?logo=langChain)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/.st-Streamlit-orange?logo=streamlit)](https://streamlit.io/)
[![FAISS](https://img.shields.io/badge/.faiss-Vector_DB-red?logo=databricks)](https://github.com/facebookresearch/faiss)
[![RAG](https://img.shields.io/badge/.-RAG-purple?logo=semanticweb)](https://www.promptingguide.ai/techniques/rag)  
[![VSCode](https://img.shields.io/badge/.vscode-VSCode-blue?logo=visualstudiocode)](https://code.visualstudio.com/)


A modular travel assistant built using **LangChain**, **Streamlit**, and **RAG** to answer flight and visa-related queries in natural language.

---

## 💡 What It Can Do

- Understand flight queries: “Refundable flights from Dubai to Tokyo around August 15?”
- Search mock flights by filters: stops, class, price, dates.
- Answer visa/refund questions using a local doc-based knowledge base.
- Powered by OpenAI, LangChain Tools, and FAISS vector DB.

---

## 🎯Quickstart
Clone Repository
```bash
git clone https://github.com/your-username/conversational-travel-assistant
cd conversational-travel-assistant
```
Install Requirements
```bash
pip install -r requirements.txt
```

### 🔑 Setup OpenAI API Key
Go to .env and add you api key for OpenAI API
```
OPENAI_API_KEY=your-api-key-here
```
### Building the FAISS Vector Store
The knowledge base (e.g., visa rules, refund policies) lives in:

```bash
📁 data/
└── visa_rules.md
You can edit this file or add more content to expand the assistant’s knowledge.
```
To build the FAISS vector store:

Open **`main.py`**

Set the flag:
```
STORE_DATA = True  # store data from new file/input
```
Run the script:
```
python main.py
```
This creates a `FAISS vector store` saved in the paiss_index/ directory.

### Run  Streamlit UI 
Once the index is built, launch the Streamlit interface:
```
streamlit run app.py
```

You can now ask questions like:

"Do I need a visa to travel from UAE to Japan?"
"What’s the refund policy for business class flights?"


## 📂 Project Structure
```
conversational-travel-assistant/
├── app.py               # Streamlit UI
├── main.py              # CLI entry (optional)
├── agent/               # LangChain tools (aviationstack, visaDB)
├── data/                # flights.json, visa_rules.md
├── flight_search/       # Custom search filters
├── utils/               # RAG utils, formatters
```

## ⚠️ Notes & Limitations
- 🧪 Prototype only — UI/UX and API tool wiring are WIP.
- 🔑 Requires OpenAI API Key.
- 📂 Mock data only; no real-time API calls yet.
- ⏳ Answers are generated using simple context-RAG without memory.

## ➡️Next Steps
 - Integrate AviationStack & Visa APIs
 - Add file upload for custom docs
 - Enable multi-turn memory (LangGraph)
 - Docker support + cloud deployment
 - Observability + logging

## 👨‍💻 Get in
Aroosh Ahmad — AI Engineer (NLP, LLMs, ML Systems)&nbsp;
[GitHub](https://github.com/arushahmd) &nbsp;• &nbsp;[LinkedIn](https://www.linkedin.com/in/arooshahmad-data/)