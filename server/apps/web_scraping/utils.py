import re


def get_price_from_description(data: str) -> int:
    new_data = re.findall(r"\d+", data)
    if new_data:
        return int("".join(new_data))
    return 0
