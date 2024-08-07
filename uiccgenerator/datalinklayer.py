from typing import List


class DataLinkLayer:

    def __init__(self, direct_convention: bool = True) -> None:
        self._start_bit: int = 0 if direct_convention else 1

    def _embed_character_frame(self, byte: int) -> List[int]:
        """
        :param byte:
        :return:
        """

        units_number = get_number_of_one_bits(byte)
        parity = (1 + units_number) % 2
        return [1, *convert_byte(byte), parity]

    def embed_character_frames(self, data: bytes) -> List[List[int]]:
        """
        :param data:
        :return:
        """

        embedded_bytes = [self._embed_character_frame(byte) for byte in data]
        print("Character framed bytes:")
        for byte in embedded_bytes:
            print(byte)
        return embedded_bytes


def convert_byte(byte: int) -> List[int]:
    bits_number = 8
    bits = []
    for _ in range(bits_number):
        bits.append(byte & 1)
        byte >>= 1
    return bits


def get_number_of_one_bits(byte: int) -> int:
    bits_number = 8
    units_number = 0
    for _ in range(bits_number):
        if byte & 1:
            units_number += 1
        byte >>= 1
    return units_number
