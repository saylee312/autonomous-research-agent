import fitz
import tempfile

from backend.rag.processors.ocr_processor import (
    extract_text_from_image
)


def process_scanned_pdf(
    pdf_path
):

    doc = fitz.open(pdf_path)

    text = []

    for page in doc:

        pix = page.get_pixmap()

        temp = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        )

        pix.save(temp.name)

        text.append(
            extract_text_from_image(
                temp.name
            )
        )

    return "\n".join(text)