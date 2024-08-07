import logging
from typing import Any, Dict
from . import utils as ut
from .apdu import APDU
from .tpdu import TPDU


logger = logging.getLogger("uicc_generator")


class UICCGenerator:
    """
    Class for working with data for UICC-Terminal interface.
    """

    def __init__(self) -> None:
        self._apdu: APDU = APDU()
        self._tpdu: TPDU = TPDU()

    def _encode_input_data(self, input_data: Dict[str, Any], t0: bool) -> None:
        """
        :param input_data: dictionary with command data to be encoded;
        :param t0: if True, then the character based transmission protocol should be used. Otherwise, the block based
        transmission protocol will be used.
        """

        for i, command_data in enumerate(input_data.get("commands", []), start=1):
            logger.info("Command #%d encoding...", i)
            try:
                apdu_encoded_command, message_case = self._apdu.encode_command(command_data)
                logger.info("Bytes after APDU: %s", apdu_encoded_command)
                tpdu_mapped_command = self._tpdu.map_bytes_from_apdu(apdu_encoded_command, message_case, t0)
                logger.info("Bytes after TPDU: %s", tpdu_mapped_command)
            except Exception as exc:
                logger.error("%s", exc)

    def run(self, input_file: str, csv: bool, t0: bool) -> None:
        """
        :param input_file: path to the json file with command names and parameters;
        :param csv: if True, then the output data should be output in CSV format;
        :param t0: if True, then the character based transmission protocol should be used. Otherwise, the block based
        transmission protocol will be used.
        """

        input_data = ut.read_json(input_file)
        self._encode_input_data(input_data, t0)
