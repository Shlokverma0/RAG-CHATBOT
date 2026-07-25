import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DOCS_PATH = "docs"
DB_PATH = "chroma_db"

def load_documents():
    documents = []
    for filename in os.listdir(DOCS_PATH):
        filepath = os.path.join(DOCS_PATH, filename)
        if filename.endswith(".pdf"):
            documents.extend(PyPDFLoader(filepath).load())
        elif filename.endswith(".txt"):
            documents.extend(TextLoader(filepath, encoding="utf-8").load())
    return documents

def main():
    documents = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_PATH)
    print("Cloud vector DB created.")

if __name__ == "__main__":
    main()