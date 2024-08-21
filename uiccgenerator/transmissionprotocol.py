class TransmissionProtocol:
    """
    Class for working with Transmission Protocol.
    """

    EDC_BYTE: bytes = (0).to_bytes(1, "big")
    MAX_INFO_FIELD_SIZE: int = 254
    NAD_BYTE: bytes = (0).to_bytes(1, "big")

    def __init__(self, t0: bool, info_field_size: int = 32) -> None:
        """
        :param t0: if True, then the character based transmission protocol should be used. Otherwise, the block based
        transmission protocol will be used;
        :param info_field_size: maximum length of the information field of blocks that can be received by the UICC.
        """

        self._info_field_size: int = max(1, min(info_field_size, TransmissionProtocol.MAX_INFO_FIELD_SIZE))
        self._t0: bool = t0

    def _encode_for_t1(self, data: bytes) -> bytes:
        """
        :param data: bytes to be converted by Transmission Protocol.
        :return: encoded bytes.
        """

        blocks = []
        while True:
            if len(data) > self._info_field_size:
                part_data = data[:self._info_field_size]
                chaining = 1
                data = data[self._info_field_size:]
            else:
                part_data = data
                chaining = 0

            pcb_byte = (chaining << 5).to_bytes(1, "big")
            length_byte = len(part_data).to_bytes(1, "big")
            blocks.append(self.NAD_BYTE + pcb_byte + length_byte + part_data + self.EDC_BYTE)
            if not chaining:
                break

        return b"".join(blocks)

    def encode(self, data: bytes) -> bytes:
        """
        :param data: bytes to be converted by Transmission Protocol.
        :return: encoded bytes.
        """

        if self._t0:
            return data

        return self._encode_for_t1(data)
