def table_to_text(table):

    if not table:
        return ""

    headers = table[0]

    rows = table[1:]

    output = []

    for row in rows:

        values = []

        for header, value in zip(
            headers,
            row
        ):

            values.append(
                f"{header}: {value}"
            )

        output.append(
            "\n".join(values)
        )

    return "\n\n".join(output)