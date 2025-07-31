from indexing.indexing_documents import build_pdf_index
from indexing.indexing_dataframe import index_dataframe
from ggsheet.get_data_ggsheet import read_sheet_data, read_multiple_sheets
import os

# sheet_key_comment = "1IGYFA6_78Ddp3idm1fZptWcQbI-8XNn8vgbA4gO256M"
# sheet_name_comment = "data"
sheet_keys = ["1IGYFA6_78Ddp3idm1fZptWcQbI-8XNn8vgbA4gO256M", "14QXmruMjMMbGds-XMLQzmzJFF2siEPg8-xogb9yqlqs"]
sheet_names = ["comment", "budget"]
json_cred = os.path.join("ggsheet", "credentials.json")

def train_all():
    print("📚 Indexing PDF documents...")
    build_pdf_index()

    print("📊 Indexing financial Google Sheet...")
    # df_comment = read_sheet_data(sheet_key_comment, sheet_name_comment, json_cred)
    # index_dataframe(df_comment, source_name="Comment")
    
    read_multiple_sheets(sheet_keys, sheet_names, json_cred)
        
    for sheet_key, sheet_name in zip(sheet_keys, sheet_names):
        df = read_sheet_data(sheet_key, sheet_name, json_cred)
        index_dataframe(df, source_name=sheet_name)

    print("✅ All indexing done.")
