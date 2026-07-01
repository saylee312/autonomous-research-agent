import fitz
import pdfplumber
import os
import uuid

from backend.rag.processors.scanned_pdf_processor import (
    process_scanned_pdf
)


def load_pdf(file_path):

    result = {
        "text": [],
        "tables": [],
        "images": []
    }

    # Text extraction
    try:

        pdf = fitz.open(
            file_path
        )

        for page in pdf:

            text = page.get_text()

            if text and text.strip():

                result["text"].append(
                    text
                )

        pdf.close()

    except Exception as e:
        logger.error(f"PDF text extraction error: {e}")

    # Table extraction
    try:

        with pdfplumber.open(
            file_path
        ) as pdf:

            for page in pdf.pages:

                tables = (
                    page.extract_tables()
                )

                for table in tables:

                    if table:

                        result[
                            "tables"
                        ].append(
                            table
                        )

    except Exception as e:
        logger.error(f"PDF table extraction error: {e}")

    # Image extraction
    try:

        pdf = fitz.open(
            file_path
        )

        image_dir = (
            "backend/storage/extracted_images"
        )

        os.makedirs(
            image_dir,
            exist_ok=True
        )

        for page in pdf:

            images = page.get_images(
                full=True
            )

            for img in images:

                try:

                    xref = img[0]

                    base_image = (
                        pdf.extract_image(
                            xref
                        )
                    )

                    image_bytes = (
                        base_image["image"]
                    )

                    image_path = os.path.join(
                        image_dir,
                        f"{uuid.uuid4().hex}.png"
                    )

                    with open(
                        image_path,
                        "wb"
                    ) as f:

                        f.write(
                            image_bytes
                        )

                    result[
                        "images"
                    ].append(
                        image_path
                    )

                except Exception as image_error:

                    logger.error(f"Image extraction error: {image_error}")

        pdf.close()

    except Exception as e:
        logger.error(f"PDF image extraction error: {e}")

    # OCR fallback
    if (
        len(result["text"]) == 0
        and len(result["tables"]) == 0
    ):

        logger.debug("Running OCR fallback for scanned PDF")

        try:

            scanned_text = (
                process_scanned_pdf(
                    file_path
                )
            )

            if (
                scanned_text
                and scanned_text.strip()
            ):

                result["text"].append(
                    scanned_text
                )

                logger.debug("OCR fallback successful")

        except Exception as e:

            logger.error(f"OCR fallback failed: {e}")

    logger.info(f"PDF parsed: text={len(result['text'])}, tables={len(result['tables'])}, images={len(result['images'])}")

    return result