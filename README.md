# 📘 Fantasy Premier League RAG Assistant

This project is a **Retrieval-Augmented Generation (RAG) system** that answers questions about **Fantasy Premier League (FPL) rules**. It combines **local FAISS embeddings** with **Google Gemini AI** to provide accurate, context-aware answers.

---

## 🔹 Features

- Splits FPL rules text into manageable chunks for retrieval  
- Generates vector embeddings of each chunk using **Sentence Transformers**  
- Stores embeddings in a **FAISS index** for fast similarity search  
- Retrieves top relevant chunks for a user question  
- Sends context to **Gemini AI** to generate answers  
- Optional retrieval metrics like similarity scores  

---

## 🛠️ Project Structure

rag-fpl-rules/
│
├─ build_index.py # Build FAISS index from FPL rules text
├─ query_rag.py # Ask questions using the RAG system
├─ data/
│ └─ fpl_help_full.txt # Source text of FPL rules
├─ chunks.json # JSON file of text chunks (ignored in Git)
├─ fpl_rules.index # FAISS index file (ignored in Git)
└─ .gitignore # Ignores venv, large files, cache


---

## ⚙️ How It Works

### 1️⃣ Build FAISS Index (`build_index.py`)

1. Reads `fpl_help_full.txt` containing the FPL rules  
2. Splits the text into overlapping chunks for better retrieval  
3. Generates embeddings for each chunk using **SentenceTransformer (`all-MiniLM-L6-v2`)**  
4. Stores the embeddings in a **FAISS index (`fpl_rules.index`)**  
5. Saves the chunked text in `chunks.json`  

✅ Output: `fpl_rules.index` + `chunks.json`  

---

### 2️⃣ Query RAG Agent (`query_rag.py`)

1. Loads FAISS index and chunked text locally  
2. Embeds the user question using the same **SentenceTransformer**  
3. Retrieves the **top 5 most similar chunks** using FAISS  
4. Sends the retrieved context + question to **Google Gemini AI**  
5. Prints the AI-generated answer  

Optional: prints similarity metrics for the retrieved chunks  

---

## ⚡ Requirements

- Python ≥ 3.10  
- `faiss-cpu`  
- `numpy`  
- `sentence-transformers`  
- `google-genai`  

Install dependencies:

```bash
pip install -r requirements.txt
```
💻 Usage
1️⃣ Build the index (run once)
python build_index.py

2️⃣ Ask questions with the agent
# Linux / Mac
export GEMINI_API_KEY="your_api_key"

# Windows (cmd)
set GEMINI_API_KEY="your_api_key"

python query_rag.py


Then type your FPL question, for example:

Ask an FPL question: How many players can I transfer per gameweek?

🗂️ Notes

chunks.json and fpl_rules.index are ignored in Git (big files)

.gitignore prevents committing your virtual environment or large files

Set your Gemini API key as an environment variable before querying

🔹 Future Improvements

Add web interface for easy question input

Include more detailed retrieval metrics

Integrate other FPL data sources like scoring rules and player stats
