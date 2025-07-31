import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

openai_api_key = st.secrets["openai"]["api_key"]
embedding_model = "text-embedding-3-small"
pdf_folder = os.path.join(BASE_DIR, "knowledge_base")
collection_name = "puppy_knowledge"

SHEET_CONFIG = {
    "1IGYFA6_78Ddp3idm1fZptWcQbI-8XNn8vgbA4gO256M": ["comment"],
    "14QXmruMjMMbGds-XMLQzmzJFF2siEPg8-xogb9yqlqs": ["budget"]
}