import os
import uuid

from backend.storage.reports.pdf_exporter import (
    export_pdf
)

from backend.storage.reports.docx_exporter import (
    export_docx
)

from backend.database.report_repository import (
    ReportRepository
)


REPORT_DIR = (
    "backend/storage/reports"
)

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


class ReportService:

    def __init__(self):

        self.repo = (
            ReportRepository()
        )

    def save_report(
        self,
        title,
        content,
        report_type="pdf"
    ):

        report_id = f"report_{uuid.uuid4().hex}"

        if report_type == "pdf":

            filepath = os.path.join(
                REPORT_DIR,
                f"{report_id}.pdf"
            )

            export_pdf(
                content,
                filepath
            )

        else:

            filepath = os.path.join(
                REPORT_DIR,
                f"{report_id}.docx"
            )

            export_docx(
                content,
                filepath
            )

        report = (
            self.repo.create_report(
                title,
                filepath,
                report_type,
                report_id,
                content
            )
        )

        return report

    def list_reports(self):

        return self.repo.list_reports()

    def delete_report(
        self,
        report_id
    ):

        report = self.repo.get_report(
            report_id
        )

        if not report:

            return False

        path = report["file_path"]

        if os.path.exists(path):

            os.remove(path)

        self.repo.delete_report(
            report_id
        )

        return True