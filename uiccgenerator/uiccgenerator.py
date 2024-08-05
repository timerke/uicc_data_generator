import logging
import os
from typing import Any, Dict
from . import utils as ut


logger = logging.getLogger("uicc_generator")


class UICCGenerator:

    def __init__(self) -> None:
        apdu_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apdu.json")
        self._apdu: Dict[str, Any] = ut.read_json(apdu_path)

    def _decode_input_data(self, input_data) -> bytes:
        """
        :param input_data:
        :return:
        """

        for command_data in input_data.get("commands", []):
            logger.info("Decode command '%s'", command_data["name"])

    def run(self, input_file: str, csv: bool) -> None:
        """
        :param input_file: path to the json file with command names and parameters;
        :param csv: if True, then the output data should be output in CSV format.
        """

        input_data = ut.read_json(input_file)
        self._decode_input_data(input_data)
