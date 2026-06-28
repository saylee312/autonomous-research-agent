from backend.rag.processors.chunker import (
    create_chunks
)

from backend.rag.processors.table_processor import (
    table_to_text
)


def build_chunks(
    document_id,
    filename,
    parsed_data
):

    final_chunks = []

    # TEXT

    for text in parsed_data["text"]:

        chunks = create_chunks(
            text
        )

        for chunk in chunks:

            final_chunks.append(
                {
                    "content": chunk,

                    "metadata": {

                        "document_id":
                        document_id,

                        "filename":
                        filename,

                        "content_type":
                        "text"
                    }
                }
            )

    # TABLES

    for table in parsed_data["tables"]:

        table_text = table_to_text(
            table
        )

        chunks = create_chunks(
            table_text
        )

        for chunk in chunks:

            final_chunks.append(
                {
                    "content": chunk,

                    "metadata": {

                        "document_id":
                        document_id,

                        "filename":
                        filename,

                        "content_type":
                        "table"
                    }
                }
            )

    # IMAGES

    for image_text in parsed_data.get(
        "image_descriptions",
        []
    ):

        chunks = create_chunks(
            image_text
        )

        for chunk in chunks:

            final_chunks.append(
                {
                    "content": chunk,

                    "metadata": {

                        "document_id":
                        document_id,

                        "filename":
                        filename,

                        "content_type":
                        "image"
                    }
                }
            )

    return final_chunks