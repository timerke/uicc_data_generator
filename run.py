import argparse
import sys
from typing import Optional
from uiccgenerator import UICCGenerator


def run(input_file: Optional[str], csv: bool) -> None:
    """
    :param input_file: path to the json file with command names and parameters;
    :param csv: if True, then the output data should be output in CSV format.
    """

    if input_file is not None:
        run_console(input_file, csv)


def run_console(input_file: str, csv: bool) -> None:
    """
    :param input_file: path to the json file with command names and parameters;
    :param csv: if True, then the output data should be output in CSV format.
    """

    generator = UICCGenerator()
    generator.run(input_file, csv)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UICC data generator")
    parser.add_argument("--input", "-i", type=str, help="Path to the json file with command names and parameters")
    parser.add_argument("--csv", action="store_true", help="Output should be in CSV format")
    parsed_args = parser.parse_args(sys.argv[1:])

    run(parsed_args.input, parsed_args.csv)
