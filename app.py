from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss


app = Flask(__name__)


embed_model = SentenceTransformer("all-MiniLM-L6-v2")


print("Loading language model... This may take a minute on first run.")
generator = pipeline(
    'text2text-generation',
    model='google/flan-t5-base',  
    device=-1  
)
print("Model loaded")

index = faiss.read_index("embeddings/faiss_index/book.index")

with open("embeddings/chunks.txt", "r", encoding="utf-8") as f:
    chunks = f.read().split("\n\n")


def retrieve_context(query, k=3, threshold=0.7):
    q_embedding = embed_model.encode([query])
    faiss.normalize_L2(q_embedding)

    distances, indices = index.search(q_embedding, k)

    relevant_chunks = []
    max_score = 0.0

    for score, idx in zip(distances[0], indices[0]):
        if idx < len(chunks):
            max_score = max(max_score, score)
            if score >= threshold:
                relevant_chunks.append(chunks[idx])

    return "\n\n".join(relevant_chunks), max_score


def generate_answer(prompt):
    try:
    
        response = generator(
            prompt,
            max_length=150,
            min_length=10,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            num_return_sequences=1
        )
        return response[0]['generated_text']
    except Exception as e:
        return f"Error generating answer: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json["query"]

    context, score = retrieve_context(user_query)
    print(score) 

    if score < 0.7 or not context.strip():
     return jsonify({"answer": "I don't know that story yet"})
    
    
    prompt = f"""Context: {context}

Question: {user_query}

Answer the question based on the context above in a friendly way for children."""

    answer = generate_answer(prompt)
    answer = answer.strip()
    
    if not answer or len(answer) < 3:
        answer = "I'm not sure about that from the story"

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
