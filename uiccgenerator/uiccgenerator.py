import csv
import logging
import sys
from typing import Any, Dict, List
from . import utils as ut
from .apdu import APDU
from .datalinklayer import DataLinkLayer
from .tpdu import TPDU
from .transmissionprotocol import TransmissionProtocol


logger = logging.getLogger("uicc_generator")


class UICCGenerator:
    """
    Class for working with data for UICC-Terminal interface.
    """

    CSV_FILE: str = "output.csv"

    def __init__(self, t0: bool, csv: bool) -> None:
        """
        :param t0: if True, then the character based transmission protocol should be used. Otherwise, the block based
        transmission protocol will be used;
        :param csv: if True, then the output data should be output in CSV format.
        """

        self._apdu: APDU = APDU()
        self._csv: bool = csv
        self._data_link_layer: DataLinkLayer = DataLinkLayer()
        self._tpdu: TPDU = TPDU(t0)
        self._transmission: TransmissionProtocol = TransmissionProtocol(t0)

    def _encode_input_data(self, input_data: Dict[str, Any]) -> List[List[List[int]]]:
        """
        :param input_data: dictionary with command data to be encoded.
        :return: list of bits for each command.
        """

        total_bits = []
        for i, command_data in enumerate(input_data.get("commands", []), start=1):
            logger.info("Command #%d encoding...", i)
            try:
                apdu_encoded_command, message_case = self._apdu.encode_command(command_data)
                logger.info("Bytes after APDU: %s", apdu_encoded_command)
                tpdu_mapped_command = self._tpdu.map_bytes_from_apdu(apdu_encoded_command, message_case)
                logger.info("Bytes after TPDU: %s", tpdu_mapped_command)
                trans_converted_command = self._transmission.convert(tpdu_mapped_command)
                logger.info("Bytes after Transmission Protocol: %s", trans_converted_command)
                embedded_bytes = self._data_link_layer.embed_character_frames(trans_converted_command)
                logger.info("Character framed bytes:")
                for byte in embedded_bytes:
                    print(byte)
                total_bits.append(embedded_bytes)
            except Exception as exc:
                logger.error("%s", exc, exc_info=sys.exc_info())
        return total_bits

    @staticmethod
    def _save_to_csv(total_bits: List[List[List[int]]]) -> None:
        """
        :param total_bits: list of bits for each command.
        """

        with open(UICCGenerator.CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(["D1"])
            for commands in total_bits:
                for command_bytes in commands:
                    for bit in command_bytes:
                        writer.writerow([bit])
            logger.info("Bits written to file '%s'", UICCGenerator.CSV_FILE)

    def decode(self, input_file: str) -> None:
        """
        :param input_file: path to the CSV-file with bits.
        """

        pass

    def encode(self, input_file: str) -> None:
        """
        :param input_file: path to the JSON-file with command names and parameters.
        """

        input_data = ut.read_json(input_file)
        total_bits = self._encode_input_data(input_data)
        if self._csv:
            self._save_to_csv(total_bits)
