class TPDU:
    """
    Class for working with Transfer Protocol Data Unit.
    """

    @staticmethod
    def _map_for_t0(data: bytes, message_case: int) -> bytes:
        """
        :param data:
        :param message_case:
        :return:
        """

        if message_case == 1:
            p3 = 0
            return data + p3.to_bytes(1, "big")

        if message_case == 4:
            return data[:-1]

        return data

    def map_bytes_from_apdu(self, data: bytes, message_case: int, t0: bool = False) -> bytes:
        """
        :param data:
        :param message_case:
        :param t0: if True, then the character based transmission protocol should be used. Otherwise, the block based
        transmission protocol will be used.
        :return:
        """

        if t0:
            return self._map_for_t0(data, message_case)

        return data
