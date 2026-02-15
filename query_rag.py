import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.genai as genai
import os

# ------------------
# LOAD LOCAL EMBEDDINGS
# ------------------
model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
index = faiss.read_index("fpl_rules.index")

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Convert chunks to list if it's a dict
if isinstance(chunks, dict):
    chunks = list(chunks.values())

# ------------------
# GEMINI CONFIG
# ------------------
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# ------------------
# ASK QUESTION
# ------------------
question = input("Ask an FPL question: ")

# Embed question locally
q_embedding = model.encode([question]).astype("float32")

# Search top 5 chunks using FAISS
k = 5
distances, indices = index.search(q_embedding, k)
indices_list = [int(i) for i in indices.flatten()]
context_chunks = [chunks[i] for i in indices_list]

# Compute similarity scores for metrics
# FAISS distances are squared L2 distances, we can convert to cosine-like similarity
similarities = 1 / (1 + distances.flatten())  # higher = more similar

# Join context
context = "\n\n".join(context_chunks)

# ------------------
# GENERATE ANSWER WITH GEMINI
# ------------------
prompt = f"""
You are an expert Fantasy Premier League assistant.
Use ONLY the context below to answer.

Context:
{context}

Question:
{question}
"""

response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents=prompt,
    config={
        "temperature": 0.2,
        "max_output_tokens": 300
    }
)

# ------------------
# PRINT ANSWER + METRICS
# ------------------
print("\n🤖 Answer:\n")
print(response.text)

#print("\n📊 Retrieval Metrics:\n")
#for i, chunk in enumerate(context_chunks):
#    print(f"Chunk {i+1} similarity: {similarities[i]:.4f}")
#    print(f"Preview: {chunk[:100]}...\n")  # first 100 chars

# Optional: answer length metric
#answer_tokens = len(response.text.split())
#print(f"Answer length (tokens): {answer_tokens}")
