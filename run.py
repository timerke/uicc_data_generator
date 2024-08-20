import argparse
import logging
import sys
from uiccgenerator import set_logger, UICCGenerator


def run(filename: str, csv: bool, t0: bool) -> None:
    """
    :param filename: path to the JSON-file with commands or CSV-file with bits;
    :param csv: if True, then encoded commands should be saved in CSV format;
    :param t0: if True, then the character based transmission protocol should be used. Otherwise, the block based
    transmission protocol will be used.
    """

    generator = UICCGenerator(t0, csv)
    if filename.lower().endswith(".json"):
        generator.encode(filename)
    elif filename.lower().endswith(".csv"):
        generator.decode(filename)
    else:
        logger = logging.getLogger("uicc_generator")
        logger.error("File '%s' has the wrong extension", filename)


if __name__ == "__main__":
    set_logger()

    parser = argparse.ArgumentParser(description="UICC data generator")
    parser.add_argument("filename", type=str, help="Path to the JSON-file with commands or CSV-file with bits")
    parser.add_argument("--csv", action="store_true", help="Encoded commands will be saved in CSV format")
    parser.add_argument("--t0", action="store_true", help="Use character based transmission protocol")
    parsed_args = parser.parse_args(sys.argv[1:])

    run(parsed_args.filename, parsed_args.csv, parsed_args.t0)
