# import os
# import pdfplumber
# from unstructured.partition.auto import partition


# def split_text(text, chunk_size=200, overlap=50):
#     words = text.split()
#     chunks = []
#     i = 0
#     while i < len(words):
#         chunk = " ".join(words[i:i+chunk_size])
#         chunks.append(chunk)
#         i += chunk_size - overlap
#     print(f"📚 Tổng số đoạn sinh ra: {len(chunks)}")
#     return chunks

# def load_documents(folder_path):
#     docs = []
#     for filename in os.listdir(folder_path):
#         path = os.path.join(folder_path, filename)
#         if not filename.lower().endswith(".pdf"):
#             continue
#         text = load_text_from_file(path)
#         chunks = split_text(text)
#         for i, chunk in enumerate(chunks):
#             docs.append({
#                 "id": f"{filename}_{i}",
#                 "content": chunk,
#                 "metadata": {"source": filename}
#             })
#     return docs

# def load_text_from_file(filepath):
#     if filepath.lower().endswith(".pdf"):
#         with pdfplumber.open(filepath) as pdf:
#             text = "\n".join([page.extract_text() or "" for page in pdf.pages])
#         print(f"📄 {os.path.basename(filepath)} - Tổng ký tự: {len(text)}")
#         return text
#     else:
#         return ""

import os
import fitz  # PyMuPDF
import uuid

def load_documents(folder_path):
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()

            chunks = split_into_chunks(text)
            for chunk in chunks:
                documents.append({
                    "id": str(uuid.uuid4()),
                    "content": chunk,
                    "metadata": {"source": filename}
                })

    return documents

def split_into_chunks(text, max_tokens=500):
    import re
    sentences = re.split(r'(\.|\!|\?)\s+', text)
    chunks, chunk = [], ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= max_tokens:
            chunk += sentence + " "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + " "
    if chunk:
        chunks.append(chunk.strip())
    return chunks