from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

PDF_INDEX = "faiss_store/pdf_index"
SHEET_INDEX = "faiss_store/sheet_index"

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def query_similar_documents(question, top_k=10):
    db = FAISS.load_local(PDF_INDEX, embeddings)
    results = db.similarity_search(question, k=top_k)
    return [r.page_content for r in results]

def query_financial_data(question, top_k=10):
    db = FAISS.load_local(SHEET_INDEX, embeddings)
    results = db.similarity_search(question, k=top_k)
    return [r.page_content for r in results]
