from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

DATA_DIR = "knowledge_base"
INDEX_DIR = "faiss_store/pdf_index"

def build_pdf_index():
    all_docs = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_DIR, file))
            pages = loader.load()
            for p in pages:
                p.metadata["source"] = file
            all_docs.extend(pages)

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=150)
    docs = splitter.split_documents(all_docs)

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(INDEX_DIR)

    print(f"✅ Indexed {len(docs)} chunks from {len(os.listdir(DATA_DIR))} PDFs.")
