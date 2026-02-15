import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ------------------
# CONFIG
# ------------------
RULES_PATH = "data/fpl_help_full.txt"
CHUNK_SIZE = 500   # characters
CHUNK_OVERLAP = 100

# ------------------
# LOAD TEXT
# ------------------
with open(RULES_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# ------------------
# CHUNKING
# ------------------
chunks = []
start = 0

while start < len(text):
    end = start + CHUNK_SIZE
    chunk = text[start:end]
    chunks.append(chunk.strip())
    start = end - CHUNK_OVERLAP

print(f"✅ Created {len(chunks)} chunks")

# Save chunks
with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

# ------------------
# EMBEDDINGS (LOCAL)
# ------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    chunks,
    show_progress_bar=True,
    convert_to_numpy=True
).astype("float32")

# ------------------
# FAISS INDEX
# ------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "fpl_rules.index")

print("✅ FAISS index saved as fpl_rules.index")
