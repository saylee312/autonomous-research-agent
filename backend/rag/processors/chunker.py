from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


splitter = (
    RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
)


def create_chunks(text):

    if text is None:
        return []

    text = str(text).strip()

    if not text:
        return []

    return splitter.split_text(
        text
    )