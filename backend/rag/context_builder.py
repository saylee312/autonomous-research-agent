def build_context(results):

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    if not documents:
        return ""

    documents = documents[0]
    metadatas = metadatas[0] if metadatas else [{}] * len(documents)

    context_blocks = []

    for doc, meta in zip(documents, metadatas):

        if not doc:
            continue

        source = meta.get("filename", "unknown")
        content_type = meta.get("content_type", "text")

        context_blocks.append(f"""
SOURCE: {source}
TYPE: {content_type}

CONTENT:
{doc}
""")

    return "\n\n".join(context_blocks)