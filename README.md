## 🧠 How it works (High Level)

1. Book text is split into chunks
2. Chunks are converted into embeddings using Sentence Transformers
3. FAISS is used to retrieve the most relevant chunks for a user query
4. A Hugging Face language model generates an answer **only from the retrieved context**
This prevents hallucinations and ensures answers stay within the book content

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Embeddings**: `sentence-transformers` (all-MiniLM-L6-v2)
- **Vector Database**: FAISS
- **LLM**: Hugging Face `google/flan-t5-base` (CPU-friendly)
- **Frontend**: HTML, CSS, JavaScript

## Run the Application
`python app.py`
Open in browser:
http://127.0.0.1:5000
