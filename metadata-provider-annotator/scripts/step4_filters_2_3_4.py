#!/usr/bin/python3

import scripts.constants as constants
import scripts.util.filter_utils as filter_utils
import scripts.util.utils as utils

INPUT_FILE = constants.NCBI_FILTER_1_OUTPUT_FILE
OUTPUT_FILE = utils.add_timestamp_to_filename(constants.NCBI_FILTER_1_OUTPUT_FILE)


def main():

    filter_utils.filter_samples_by_attributes(constants.ROOT_FOLDER_NAME, INPUT_FILE,
                                              constants.NCBI_FILTER_2_OUTPUT_FILE,
                                              constants.NCBI_FILTER_2_SPECS,
                                              constants.NCBI_ATT_NAMES_VALUES_VARIATIONS, 10000)

    filter_utils.filter_samples_by_attributes(constants.ROOT_FOLDER_NAME, INPUT_FILE,
                                              constants.NCBI_FILTER_3_OUTPUT_FILE,
                                              constants.NCBI_FILTER_3_SPECS,
                                              constants.NCBI_ATT_NAMES_VALUES_VARIATIONS, 10000)

    filter_utils.filter_samples_by_attributes(constants.ROOT_FOLDER_NAME, INPUT_FILE,
                                              constants.NCBI_FILTER_4_OUTPUT_FILE,
                                              constants.NCBI_FILTER_4_SPECS,
                                              constants.NCBI_ATT_NAMES_VALUES_VARIATIONS, 10000)


if __name__ == "__main__":
    main()
