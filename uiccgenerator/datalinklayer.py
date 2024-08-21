from typing import List


class DataLinkLayer:
    """
    Class for working as Data link layer.
    """

    def __init__(self, direct_convention: bool = True) -> None:
        """
        :param direct_convention: depending upon the convention used, the logical '1' in a character is either
        represented by state H on the I/O line, direct convention, or state L on the I/O line, inverse convention.
        """

        self._start_bit: int = 0 if direct_convention else 1

    @staticmethod
    def _embed_character_frame(byte: int) -> List[int]:
        """
        :param byte: the value of the byte to be wrapped in bits.
        :return: list of bits (leading bit, bits of the given byte and parity bit).
        """

        units_number = get_number_of_one_bits(byte)
        parity = (1 + units_number) % 2
        return [1, *convert_byte_to_bits(byte), parity]

    def embed_character_frames(self, data: bytes) -> List[List[int]]:
        """
        :param data: an array of bytes, each of which needs to be wrapped in a leading bit and a parity bit.
        :return: list of bits to which the given byte array is converted.
        """

        embedded_bytes = [self._embed_character_frame(byte) for byte in data]
        return embedded_bytes

    @staticmethod
    def remove_character_frames(bits: List[int]) -> int:
        """
        :param bits: list of bits from which to remove leading bit and parity bit.
        :return: byte value without leading bit and parity bit.
        """

        if bits[0] != 1:
            raise ValueError("No leading bit 1")

        if bits[:-1].count(1) % 2 != bits[-1]:
            raise ValueError("Invalid parity bit")

        return convert_bits_to_byte(bits[1:-1])


def convert_bits_to_byte(bits: List[int]) -> int:
    """
    :param bits: list of bits.
    :return: byte representation of a given list of bits.
    """

    byte = 0
    for i, bit in enumerate(bits):
        byte |= bit
        if i < len(bits) - 1:
            byte <<= 1
    return byte


def convert_byte_to_bits(byte: int) -> List[int]:
    """
    :param byte: byte value.
    :return: representation of a byte as a list of bits.
    """

    bits_number = 8
    bits = [0] * bits_number
    b = byte
    for i in range(bits_number - 1, -1, -1):
        bits[i] = byte & 1
        byte >>= 1
    return bits


def get_number_of_one_bits(byte: int) -> int:
    """
    :param byte: byte value.
    :return: number of bit units in a byte.
    """

    bits_number = 8
    units_number = 0
    for _ in range(bits_number):
        if byte & 1:
            units_number += 1
        byte >>= 1
    return units_number
