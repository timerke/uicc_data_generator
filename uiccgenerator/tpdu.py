class TPDU:
    """
    Class for working with Transfer Protocol Data Unit.
    """

    def __init__(self, t0: bool) -> None:
        """
        :param t0: if True, then the character based transmission protocol should be used. Otherwise, the block based
        transmission protocol will be used.
        """

        self._t0: bool = t0

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

    def map_bytes_from_apdu(self, apdu_data: bytes, message_case: int) -> bytes:
        """
        :param apdu_data: bytes after APDU;
        :param message_case: message case.
        :return: bytes mapped to TPDU.
        """

        if self._t0:
            return self._map_for_t0(apdu_data, message_case)

        return apdu_data
