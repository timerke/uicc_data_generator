import csv
import json
from typing import Any, Dict, List


def read_csv(input_file: str) -> List[int]:
    """
    :param input_file: path to the CSV-file with encoded bits.
    :return: list with bit values from file.
    """

    bits = []
    with open(input_file, newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for i, row in enumerate(reader):
            if i == 0:
                continue

            bits.append(int(row[0]))

    return bits


def read_json(input_file: str) -> Dict[str, Any]:
    """
    :param input_file: path to the JSON-file with command names and parameters.
    :return: dictionary with data from file.
    """

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
