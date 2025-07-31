# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from bot_config.config import SHEET_CONFIG
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

@lru_cache(maxsize=1)
def query_from_multiple_sheets(question, top_k=5):
    results = []
    all_raw_documents = []
    for sheet_key, sheet_names in SHEET_CONFIG.items():
        for sheet_name in sheet_names:
            index_path = f"faiss_store/{sheet_name}_index"
            db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
            # result = db.similarity_search(question, k=top_k)
            # results.extend(result)
            
            current_sheet_results = db.similarity_search(question, k=top_k)
            all_raw_documents.extend(current_sheet_results)
    
    # return results
    return [doc.page_content for doc in all_raw_documents]