# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from functools import lru_cache

PDF_INDEX = "faiss_store/pdf_index"
SHEET_INDEX = "faiss_store/sheet_index"

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")



@lru_cache(maxsize=1)
def get_pdf_db():
    return FAISS.load_local(PDF_INDEX, embeddings)

@lru_cache(maxsize=1)
def query_similar_documents(question, top_k=5):
    db = FAISS.load_local(PDF_INDEX, embeddings, allow_dangerous_deserialization=True)
    results = db.similarity_search(question, k=top_k)
    return [r.page_content for r in results]

def query_financial_data(question, top_k=5):
    db = FAISS.load_local(SHEET_INDEX, embeddings, allow_dangerous_deserialization=True)
    results = db.similarity_search(question, k=top_k)
    return [r.page_content for r in results]
