import uuid

from datetime import datetime, UTC

from backend.database.mongo import db


def serialize_doc(doc):
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]


class ReportRepository:

    def __init__(self):

        self.collection = db["reports"]

    def create_report(
        self,
        title,
        file_path,
        report_type,
        report_id=None,
        content=None
    ):

        if report_id is None:
            report_id = f"report_{uuid.uuid4().hex}"

        report = {

            "_id": report_id,

            "title": title,

            "file_path": file_path,

            "report_type": report_type,

            "content": content,

            "created_at": datetime.now(UTC)
        }

        self.collection.insert_one(
            report
        )
        
        print(f"[DEBUG] Saved report: ID={report_id}, title={title}, content_len={len(content) if content else 0}")

        return report

    def get_report(
        self,
        report_id
    ):

        return self.collection.find_one(
            {"_id": report_id}
        )

    def list_reports(self):

        reports = list(
            self.collection.find().sort(
                "created_at",
                -1
            )
        )
        
        return serialize_docs(reports)

    def delete_report(
        self,
        report_id
    ):

        self.collection.delete_one(
            {"_id": report_id}
        )