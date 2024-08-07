class TPDU:
    """
    Class for working with Transfer Protocol Data Unit.
    """

    @staticmethod
    def _map_for_t0(apdu_data: bytes, message_case: int) -> bytes:
        """
        :param apdu_data: bytes after APDU;
        :param message_case: message case.
        :return:
        """

        if message_case == 1:
            p3 = 0
            return apdu_data + p3.to_bytes(1, "big")

        if message_case == 4:
            return apdu_data[:-1]

        return apdu_data

    def map_bytes_from_apdu(self, apdu_data: bytes, message_case: int, t0: bool = False) -> bytes:
        """
        :param apdu_data: bytes after APDU;
        :param message_case: message case;
        :param t0: if True, then the character based transmission protocol should be used. Otherwise, the block based
        transmission protocol will be used.
        :return: bytes mapped to TPDU.
        """

        if t0:
            return self._map_for_t0(apdu_data, message_case)

        return apdu_data
