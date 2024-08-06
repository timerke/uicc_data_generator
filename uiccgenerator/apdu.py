import logging
import os
from typing import Any, Dict, List, Optional
from . import utils as ut


logger = logging.getLogger("uicc_generator")


class IncorrectDataException(Exception):
    pass


class APDU:
    """
    Class for working with Application Protocol Data Unit.
    """

    def __init__(self) -> None:
        apdu_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apdu.json")
        self._json_data: Dict[str, Any] = ut.read_json(apdu_path)["contents"]
        self.__convert_instruction_codes_to_int()

    @property
    def body(self) -> Dict[str, Any]:
        return self._json_data["message_structure"]["body"]

    @property
    def commands(self) -> Dict[str, Any]:
        return self._json_data["commands"]

    @property
    def message_cases(self) -> List[List[str]]:
        return self._json_data["cases"]

    @property
    def header(self) -> Dict[str, Any]:
        return self._json_data["message_structure"]["header"]

    def __convert_instruction_codes_to_int(self) -> None:

        def to_int(x: str) -> int:
            return int(x, base=16)

        for command in self.commands.values():
            if isinstance(command["INS"], list):
                command["INS"] = list(map(to_int, command["INS"]))
            else:
                command["INS"] = to_int(command["INS"])

    def _check_command_data(self, command_data: Dict[str, Any]) -> None:
        """
        :param command_data: dictionary with fields of the command to be checked.
        """

        message_cases = self._get_command_cases(command_data["name"])
        total_missing_fields = dict()
        min_missing_fields = None
        for message_case in message_cases[::-1]:
            missing_fields = []
            for field in message_case:
                if field not in command_data:
                    missing_fields.append(field)

            if missing_fields:
                total_missing_fields[",".join(message_case)] = missing_fields
                if min_missing_fields is None or len(missing_fields) < len(min_missing_fields):
                    min_missing_fields = missing_fields

        if len(total_missing_fields) == len(message_cases):
            raise IncorrectDataException(f"There are not enough fields for the '{command_data['name']}' command: "
                                         f"{', '.join(min_missing_fields)}")

    def _check_command_name(self, command_data: Dict[str, Any]) -> None:
        """
        :param command_data: dictionary with fields of the command to be checked.
        """

        command_name = None
        if "name" in command_data:
            command_name = command_data["name"].upper()
        elif "INS" in command_data:
            command_name = self._get_command_name(command_data["INS"])

        if command_name is None:
            raise IncorrectDataException(f"The command could not be determined for the data: {command_data}")

        if command_name not in self.commands:
            supported_commands = ", ".join(self.commands.keys())
            raise IncorrectDataException(f"The command '{command_name}' is not supported. Available commands: "
                                         f"{supported_commands}")

        if "name" in command_data and "INS" in command_data:
            if command_name != self._get_command_name(command_data["INS"]):
                logger.warning("Invalid instruction code '%s' specified for '%s' command. The incorrect value "
                               "will be replaced with the correct one '%s'", command_data["INS"], command_name,
                               self.commands[command_name]["INS"])
                command_data["INS"] = self.commands[command_name]["INS"]

        command_data["name"] = command_name

    def _convert_command_data_to_int(self, command_data: Dict[str, Any]) -> None:
        """
        Method converts command fields to integer values.
        :param command_data: dictionary with fields of the command.
        """

        for key, value in command_data.items():
            if (key in self.header or key in self.body) and isinstance(value, str):
                try:
                    command_data[key] = int(value, base=16)
                except ValueError as exc:
                    logger.error("Failed to convert '%s' field: %s", key, exc)

    def _encode_body(self, command_data: Dict[str, Any]) -> bytes:
        """
        :param command_data: dictionary with fields of the command to be encoded.
        :return: encoded command body.
        """

        return encode(self.body, command_data)

    def _encode_header(self, command_data: Dict[str, Any]) -> bytes:
        """
        :param command_data: dictionary with fields of the command to be encoded.
        :return: encoded command header.
        """

        return encode(self.header, command_data)

    def _get_command_cases(self, command_name: str) -> List[List[str]]:
        """
        :param command_name: command name.
        :return: possible message cases for a given command.
        """

        command_data = self.commands[command_name]
        case_indexes = command_data["cases"]
        return [self.message_cases[i] for i in case_indexes]

    def _get_command_name(self, instruction_code: int) -> Optional[str]:
        """
        :param instruction_code: instruction code of command.
        :return: command name.
        """

        for command, description in self.commands.items():
            if isinstance(description["INS"], list):
                if instruction_code in description["INS"]:
                    return command
            elif instruction_code == description["INS"]:
                return command

        return None

    def encode_command(self, command_data: Dict[str, Any]) -> bytes:
        """
        :param command_data: dictionary with fields of the command to be encoded.
        :return: encoded command.
        """

        self._convert_command_data_to_int(command_data)
        self._check_command_name(command_data)
        self._check_command_data(command_data)
        logger.info("'%s' command encoding...", command_data["name"])
        return self._encode_header(command_data) + self._encode_body(command_data)


def encode(fields: Dict[str, Any], command_data: Dict[str, Any]) -> bytes:
    """
    :param fields:
    :param command_data: dictionary with fields of the command to be encoded.
    :return: encoded message.
    """

    encoded_values = []
    for name, description in fields.items():
        if name in command_data:
            value = command_data[name]
            encoded_values.append(value.to_bytes(description["length"], "big"))
    return b"".join(encoded_values)
