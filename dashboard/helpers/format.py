def format_number(value: int) -> str:
    """
    Formats large numbers with 'k', 'kk', etc. notation.

    :param value: The number to be formatted.
    :return: A string representation of the number in a formatted style, 
             using 'k' for thousands and 'kk' for millions.
    """
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}kk"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}k"
    else:
        return str(value)

