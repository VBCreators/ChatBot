from pathlib import Path
from langchain_core.documents import Document
from langchain_docling import DoclingLoader


def rag_loader(DOC_PATH: Path) -> list[Document]:

    extension = DOC_PATH.suffix.lower()

    if extension in {".pptx", ".pdf", ".md", "docx", ".csv"}:
        return load_using_docling(DOC_PATH)

    elif extension == ".txt":
        return load_text(DOC_PATH)


def load_using_docling(DOC_PATH: Path) -> list[Document]:
    return DoclingLoader(file_path=DOC_PATH).load()


# Text Loader


def load_text(DOC_PATH: Path) -> list[Document]:
    text = DOC_PATH.read_text(
        encoding="utf-8",
    )
    return [
        Document(
            pagecontent=text,
            metadata={
                "sourc": str(DOC_PATH),
                "file_type": "txt",
            },
        )
    ]
