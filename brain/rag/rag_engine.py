from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv


from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import MODEL_NAME, GOOGLE_API_KEY, MAX_TOKENS
from brain.rag.rag_services.loader_service import rag_loader
from brain.rag.rag_services.splitter_service import rag_splitter


load_dotenv()

DOC_PATH = Path(__file__).parent.parent.parent / "data" / "raw" / "handbook.md"
INDEX_DIR = Path(__file__).parent.parent.parent / "data" / "faiss_index"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL = MODEL_NAME


def build_index() -> FAISS:

    # Step 1 : Loading Document
    documents = rag_loader(DOC_PATH)

    # Step 2 : Chunking Document

    # print("Step 2 of 4: Splitting into chunks...")

    # splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=1000,
    #     chunk_overlap=200,
    # )
    # chunks = splitter.split_documents(documents)
    # print(f"      -> {len(chunks)} chunks produced.")

    chunks = rag_splitter(documents)

    # Step 3 : Embedding

    print(f"Step 3 of 4: Embedding chunks with {EMBEDDING_MODEL_NAME}...")

    embedding = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # Step 4 : Vector Store

    print(f"Step 4 of 4: Building FAISS index, saving to {INDEX_DIR}...")

    vectorstore = FAISS.from_documents(chunks, embedding)
    vectorstore.save_local(str(INDEX_DIR))
    print("      -> Index built and saved.")
    return vectorstore


# PHASE 2 — RETRIEVAL + GENERATION (online, run per query)


def format_docs(docs) -> str:
    return "\n\n --- \n\n".join(doc.page_content for doc in docs)


def build_rag_chain(vectorestore: FAISS):

    # RETRIEVER
    retriever = vectorestore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and fill it in."
        )

    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=0,
        max_output_tokens=MAX_TOKENS,
        google_api_key=GOOGLE_API_KEY,
    )

    prompt = ChatPromptTemplate([
        (
            "system",
            "You are a precise assistant. Answer the user's question "
            "using ONLY the context provided below. If the context does "
            "not contain the answer, reply exactly: "
            "'I don't know based on the provided context.' "
            "Always cite the relevant context using [source: <id>] notation.\n\n"
            "Context:\n{context}",
        ),
        ("human", "{question}"),
    ])

    rag_chain = (
        RunnablePassthrough.assign(
            context=(lambda x: x["question"]) | retriever | format_docs,
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def main() -> None:

    build_index()

    # if not INDEX_DIR.exists():
    #     vectorstore = build_index()

    # print(f"loading existing index from {INDEX_DIR}...")

    # embeddings = HuggingFaceEmbeddings(
    #     model_name=EMBEDDING_MODEL_NAME,
    #     model_kwargs={"device": "cpu"},
    #     encode_kwargs={"normalize_embeddings": True},
    # )

    # vectorstore = FAISS.load_local(
    #     str(INDEX_DIR),
    #     embeddings,
    #     allow_dangerous_deserialization=True,
    # )

    # chain = build_rag_chain(vectorstore)

    # questions = [
    #     "What is the name of the company's flagship product?",
    #     "Who is the CTO?",
    #     "What is the weather like in Paris tomorrow?",
    # ]

    # for q in questions:
    #     print(f"\nQ: {q}")
    #     answer = chain.invoke({"question": q})
    #     print(f"A: {answer}")
    # # print("\n\nanswre is {answer}")


if __name__ == "__main__":
    main()
