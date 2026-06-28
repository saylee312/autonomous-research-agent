import fitz
import tempfile
import os

from backend.rag.processors.ocr_processor import (
    extract_text_from_image
)


def process_scanned_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    extracted_text = []

    try:

        for page in doc:

            pix = page.get_pixmap()

            temp = tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            )

            temp_path = temp.name

            temp.close()

            pix.save(temp_path)

            try:

                text = extract_text_from_image(
                    temp_path
                )

                if text and text.strip():

                    extracted_text.append(
                        text
                    )

            finally:

                if os.path.exists(
                    temp_path
                ):
                    os.remove(
                        temp_path
                    )

    finally:

        doc.close()

    return "\n".join(
        extracted_text
    )