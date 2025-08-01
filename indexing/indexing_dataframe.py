from langchain.schema import Document
# from langchain.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import pandas as pd
import os

INDEX_DIR = "faiss_store/sheet_index"

def index_dataframe(df: pd.DataFrame, source_name="google_sheet"):
    docs = []
    for i, row in df.iterrows():
        text = ", ".join(f"{col}: {row[col]}" for col in row.index)
        metadata = {"row_index": i, "source": source_name}
        docs.append(Document(page_content=text, metadata=metadata))

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    db = FAISS.from_documents(docs, embeddings)

    index_path = f"faiss_store/{source_name}_index"
    db.save_local(index_path)

    print(f"✅ Indexed {len(docs)} rows from {source_name} into FAISS.")
