from backend.rag.processors.ocr_processor import (
    extract_text_from_image
)

from backend.rag.processors.image_processor import (
    generate_caption
)


def understand_image(
    image_path
):

    ocr_text = (
        extract_text_from_image(
            image_path
        )
    )

    caption = (
        generate_caption(
            image_path
        )
    )

    return f"""
IMAGE DESCRIPTION:

{caption}

OCR TEXT:

{ocr_text}
"""