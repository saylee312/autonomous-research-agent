from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def export_pdf(
    content,
    output_path
):

    doc = SimpleDocTemplate(
        output_path
    )

    styles = getSampleStyleSheet()

    elements = [

        Paragraph(
            content.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    ]

    doc.build(elements)