from indexing.indexing_documents import build_pdf_index
from indexing.indexing_dataframe import index_dataframe
from ggsheet.get_data_ggsheet import read_sheet_data
import os

sheet_key = "1IGYFA6_78Ddp3idm1fZptWcQbI-8XNn8vgbA4gO256M"
sheet_name = "data"
json_cred = os.path.join("ggsheet", "credentials.json")

def train_all():
    print("📚 Indexing PDF documents...")
    build_pdf_index()

    print("📊 Indexing financial Google Sheet...")
    df = read_sheet_data(sheet_key, sheet_name, json_cred)
    index_dataframe(df, source_name="GoogleSheet")

    print("✅ All indexing done.")
