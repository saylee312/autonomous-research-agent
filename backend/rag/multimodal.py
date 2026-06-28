import os

from backend.rag.loaders.pdf_loader import (
    load_pdf
)

from backend.rag.loaders.docx_loader import (
    load_docx
)

from backend.rag.loaders.pptx_loader import (
    load_pptx
)

from backend.rag.loaders.csv_loader import (
    load_csv
)

from backend.rag.loaders.excel_loader import (
    load_excel
)

from backend.rag.loaders.image_loader import (
    load_image
)


def load_document(file_path):

    ext = os.path.splitext(
        file_path
    )[1].lower()

    if ext == ".pdf":

        return load_pdf(file_path)

    elif ext == ".docx":

        return load_docx(file_path)

    elif ext == ".pptx":

        return load_pptx(file_path)

    elif ext == ".csv":

        return load_csv(file_path)

    elif ext in [
        ".xlsx",
        ".xls"
    ]:

        return load_excel(file_path)

    elif ext in [

        ".png",
        ".jpg",
        ".jpeg"
    ]:

        return load_image(file_path)

    raise ValueError(
        f"Unsupported file: {ext}"
    )