# import os
# import chromadb
# from openai import OpenAI
# from config import openai_api_key

# # Khởi tạo client cho Chroma (chuẩn mới nhất)
# # chroma_client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), "../.chroma_store"))
# from chromadb.config import Settings

# chroma_client = chromadb.Client(Settings(
#     chroma_db_impl="duckdb+parquet",
#     persist_directory=None
# ))
# # Định nghĩa collection
# collection = chroma_client.get_or_create_collection(name="meoz_knowledge")

# # Khởi tạo OpenAI client
# client = OpenAI(api_key=openai_api_key)

# def get_embedding(text):
#     response = client.embeddings.create(
#         input=[text],
#         model="text-embedding-3-small"
#     )
#     return response.data[0].embedding

# def add_documents(docs):
#     print(f"📋 Tổng số đoạn sinh ra: {len(docs)}")
#     for doc in docs:
#         embedding = get_embedding(doc["content"])
#         print(f"➕ Thêm đoạn ID: {doc['id']}, ký tự: {len(doc['content'])}")
#         collection.add(
#             documents=[doc["content"]],
#             embeddings=[embedding],
#             metadatas=[doc["metadata"]],
#             ids=[doc["id"]]
#         )

# def query_similar_documents(question, n_results=5):
#     embedding = get_embedding(question)
#     results = collection.query(query_embeddings=[embedding], n_results=n_results)

#     docs = results.get("documents", [[]])[0]
#     metas = results.get("metadatas", [[]])[0]

#     if not docs:
#         print("⚠️ No related documents found.")
#     else:
#         print(f"\n🌟 {len(docs)} đoạn được truy vấn:")
#         for i, d in enumerate(docs):
#             print(f"[{i+1}] {d[:150]}...")
#             print(f"    📁 Source: {metas[i].get('source')}\n")

#     return docs

# def reset_collection():
#     chroma_client.delete_collection(name="meoz_knowledge")
#     print("🗑️ Đã xóa collection cũ.")


## -------------------------------------------------------------------------------- ##

import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

index_path = os.path.join(os.path.dirname(__file__), "faiss_index")
data_path = os.path.join(os.path.dirname(__file__), "faiss_data.pkl")

# model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("BAAI/bge-small-en-v1.5")  # hoặc multi-qa-MiniLM-L6-cos-v1

if os.path.exists(index_path):
    index = faiss.read_index(index_path)
    with open(data_path, "rb") as f:
        documents = pickle.load(f)
else:
    index = faiss.IndexFlatL2(384)
    documents = []

def add_documents(docs):
    global documents
    texts = [doc["content"] for doc in docs]
    embeddings = model.encode(texts)
    index.add(np.array(embeddings).astype("float32"))
    documents.extend(docs)

    # Save
    faiss.write_index(index, index_path)
    with open(data_path, "wb") as f:
        pickle.dump(documents, f)

def query_similar_documents(query, top_k=8):
    if len(documents) == 0:
        print("⚠️ Chưa có dữ liệu trong FAISS index.")
        return []

    embedding = model.encode([query])
    distances, indices = index.search(np.array(embedding).astype("float32"), top_k)
    return [documents[i]["content"] for i in indices[0] if i < len(documents)]

