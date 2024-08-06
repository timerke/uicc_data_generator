import argparse
import sys
from typing import Optional
from uiccgenerator import set_logger, UICCGenerator


def run(input_file: Optional[str], csv: bool, t0: bool) -> None:
    """
    :param input_file: path to the json file with command names and parameters;
    :param csv: if True, then the output data should be output in CSV format;
    :param t0: if True, then you need to use the character based transmission protocol.
    """

    if input_file is not None:
        run_console(input_file, csv, t0)


def run_console(input_file: str, csv: bool, t0: bool) -> None:
    """
    :param input_file: path to the json file with command names and parameters;
    :param csv: if True, then the output data should be output in CSV format;
    :param t0: if True, then you need to use the character based transmission protocol.
    """

    generator = UICCGenerator()
    generator.run(input_file, csv, t0)


if __name__ == "__main__":
    set_logger()

    parser = argparse.ArgumentParser(description="UICC data generator")
    parser.add_argument("--input", "-i", type=str, help="Path to the json file with command names and parameters")
    parser.add_argument("--csv", action="store_true", help="Output should be in CSV format")
    parser.add_argument("--t0", action="store_true", help="Use character based transmission protocol")
    parsed_args = parser.parse_args(sys.argv[1:])

    run(parsed_args.input, parsed_args.csv, parsed_args.t0)
