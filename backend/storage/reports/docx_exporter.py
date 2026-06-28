from docx import Document


def export_docx(
    content,
    output_path
):

    doc = Document()

    doc.add_paragraph(
        content
    )

    doc.save(
        output_path
    )