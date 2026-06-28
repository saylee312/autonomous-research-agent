def calculator(expression: str):

    try:

        return str(
            eval(
                expression,
                {"__builtins__": {}},
                {}
            )
        )

    except Exception as e:

        return str(e)