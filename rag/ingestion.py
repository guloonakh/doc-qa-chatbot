import os
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBED_MODEL = "all-MiniLM-L6-v2"
INDEX_PATH  = "faiss_index"

def load_and_index_pdf(pdf_bytes: bytes) -> FAISS:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if text.strip():
            pages.append({"text": text, "page": page_num})

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = []
    metadatas = []
    for p in pages:
        for chunk in splitter.split_text(p["text"]):
            chunks.append(chunk)
            metadatas.append({"page": p["page"]})

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = FAISS.from_texts(chunks, embeddings, metadatas=metadatas)
    vectorstore.save_local(INDEX_PATH)
    return vectorstore


def load_existing_index() -> FAISS | None:
    if os.path.exists(INDEX_PATH):
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        return FAISS.load_local(INDEX_PATH, embeddings,
                                allow_dangerous_deserialization=True)
    return None