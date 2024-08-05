import logging
from . import utils as ut
from .apdu import APDU


logger = logging.getLogger("uicc_generator")


class UICCGenerator:

    def __init__(self) -> None:
        self._apdu: APDU = APDU()

    def _encode_input_data(self, input_data) -> bytes:
        """
        :param input_data:
        :return:
        """

        for command_data in input_data.get("commands", []):
            try:
                encoded_command = self._apdu.encode_command(command_data)
                logger.info("Encoded command: %s", encoded_command)
            except Exception as exc:
                logger.error("%s", exc)

    def run(self, input_file: str, csv: bool) -> None:
        """
        :param input_file: path to the json file with command names and parameters;
        :param csv: if True, then the output data should be output in CSV format.
        """

        input_data = ut.read_json(input_file)
        self._encode_input_data(input_data)
