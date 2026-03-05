from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import ollama

# embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_vector_store(chunks):

    texts = [c["text"] for c in chunks]

    embeddings = model.encode(texts)

    embeddings = np.array(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def retrieve(question, index, chunks, k=2):

    question_embedding = model.encode([question])

    distances, indices = index.search(
        np.array(question_embedding),
        k
    )

    contexts = []

    for idx in indices[0]:
        contexts.append(chunks[idx])

    return contexts


def generate_answer(question, contexts):

    context_text = ""

    for c in contexts:
        context_text += f"(Page {c['page']}): {c['text']}\n"

    prompt = f"""
Answer ONLY using the notes below.

Notes:
{context_text[:1500]}

Question: {question}

If the answer is not in the notes say:
"I don't have enough information."
"""

    response = ollama.chat(
        model="phi",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]