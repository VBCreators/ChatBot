from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def rag_splitter(documents: list[Document]) -> list[Document]:

    chunk_size = 1000
    chunk_overlap = 250
    splitter = create_rag_splitter(chunk_size, chunk_overlap)

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    return chunks


def create_rag_splitter(
    chunk_size: int = 1000, chunk_overlap: int = 200
) -> RecursiveCharacterTextSplitter:

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
