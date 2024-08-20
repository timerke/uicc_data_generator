import json
from typing import Any, Dict


def read_json(input_file: str) -> Dict[str, Any]:
    """
    :param input_file: path to the JSON-file with command names and parameters.
    """

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
