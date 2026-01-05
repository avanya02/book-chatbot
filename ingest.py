from sentence_transformers import SentenceTransformer
import faiss
import os

# Load book
with open("data/book.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Chunk text
def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks

chunks = chunk_text(text)

# Embedding model (FREE & lightweight)
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

# Store in FAISS
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

os.makedirs("embeddings/faiss_index", exist_ok=True)
faiss.write_index(index, "embeddings/faiss_index/book.index")

# Save chunks
with open("embeddings/chunks.txt", "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(chunk + "\n\n")

print("✅ Book ingestion completed.")
