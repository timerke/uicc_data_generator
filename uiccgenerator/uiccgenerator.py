from . import utils as ut


class UICCGenerator:

    def run(self, input_file: str, csv: bool) -> None:
        """
        :param input_file: path to the json file with command names and parameters;
        :param csv: if True, then the output data should be output in CSV format.
        """

        data = ut.read_json(input_file)
        print(data)
