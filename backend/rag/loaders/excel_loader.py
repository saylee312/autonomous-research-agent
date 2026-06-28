import pandas as pd


def load_excel(file_path):

    sheets = pd.read_excel(
        file_path,
        sheet_name=None
    )

    tables = []

    for _, df in sheets.items():

        tables.append(
            df.values.tolist()
        )

    return {

        "text": [],

        "tables": tables,

        "images": []
    }