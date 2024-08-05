import os
from typing import Any, Dict
from . import utils as ut


class APDUEncoder:

    def __init__(self) -> None:
        apdu_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apdu.json")
        self._apdu: Dict[str, Any] = ut.read_json(apdu_path)["contents"]

    def _encode_body(self, command_data: Dict[str, Any]) -> bytes:
        return encode(self._apdu["body"], command_data)

    def _encode_header(self, command_data: Dict[str, Any]) -> bytes:
        return encode(self._apdu["header"], command_data)

    def encode_command(self, command_data: Dict[str, Any]) -> bytes:
        """
        :param command_data:
        :return:
        """

        return self._encode_header(command_data) + self._encode_body(command_data)


def encode(fields: Dict[str, Any], command_data: Dict[str, Any]) -> bytes:
    encoded_values = []
    for field_name, field_description in fields.items():
        if field_name in command_data:
            field_value = int(command_data[field_name], base=16)
            encoded_values.append(field_value.to_bytes(field_description["length"], "big"))
    return b"".join(encoded_values)
