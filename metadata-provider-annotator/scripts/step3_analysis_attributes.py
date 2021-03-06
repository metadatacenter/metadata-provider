#!/usr/bin/python3

# Utility to perform a preliminary analysis on the frequency of attribute names and attribute values in BioSample

import scripts.constants as constants
import xml.dom.pulldom as pulldom
import xml.etree.ElementTree as ET
import gzip
import scripts.util.utils as utils
import os

INPUT_FILE = constants.NCBI_ANALYSIS_ATT_NAMES_FILTER_1_INPUT_FILE
OUTPUT_FILE_ATTRIBUTE_NAMES = constants.NCBI_ANALYSIS_OUTPUT_FILE_ATTRIBUTE_NAMES
OUTPUT_FILE_DISPLAY_NAMES = constants.NCBI_ANALYSIS_OUTPUT_FILE_DISPLAY_NAMES
OUTPUT_FILE_HARMONIZED_NAMES = constants.NCBI_ANALYSIS_OUTPUT_FILE_HARMONIZED_NAMES
OUTPUT_FILE_ALL_NAMES = constants.NCBI_ANALYSIS_OUTPUT_FILE_ALL_NAMES
LOG_FREQUENCY = 100000


def main():
    print('Input file: ' + INPUT_FILE)
    print('Processing NCBI samples...')
    input_file_extension = os.path.splitext(INPUT_FILE)[1]
    # Read biosamples from XML file
    if input_file_extension == 'gz':
        content = pulldom.parse(gzip.open(INPUT_FILE))
    else:
        content = pulldom.parse(INPUT_FILE)

    processed_samples_count = 0

    attribute_names_count = {}
    display_names_count = {}
    harmonized_names_count = {}
    all_names_count = {}

    for event, node in content:
        if event == 'START_ELEMENT' and node.tagName == 'BioSample':
            content.expandNode(node)
            xml_sample = node.toxml()
            biosample_node = ET.fromstring(xml_sample)
            attributes = biosample_node.find('Attributes')
            if attributes is not None:
                for att in attributes:
                    # Attribute name
                    attribute_name = str(att.get('attribute_name'))

                    if attribute_name not in attribute_names_count:
                        attribute_names_count[attribute_name] = 1
                    else:
                        attribute_names_count[attribute_name] = attribute_names_count[attribute_name] + 1

                    # Display name
                    display_name = str(att.get('display_name'))

                    if display_name not in display_names_count:
                        display_names_count[display_name] = 1
                    else:
                        display_names_count[display_name] = display_names_count[display_name] + 1

                    # Harmonized name
                    harmonized_name = str(att.get('harmonized_name'))

                    if harmonized_name not in harmonized_names_count:
                        harmonized_names_count[harmonized_name] = 1
                    else:
                        harmonized_names_count[harmonized_name] = harmonized_names_count[harmonized_name] + 1

                    # String with attribute name, display name, and harmonized name
                    att_str = attribute_name + '|' + display_name + '|' + harmonized_name

                    if att_str not in all_names_count:
                        all_names_count[att_str] = 1
                    else:
                        all_names_count[att_str] = all_names_count[att_str] + 1

            else:
                print('No attributes for this sample')

            processed_samples_count = processed_samples_count + 1

            if processed_samples_count % LOG_FREQUENCY == 0:
                print('Processed samples: ' + str(processed_samples_count))

    # Sort by count
    sorted_attribute_names_count = utils.sort_dict_by_values(attribute_names_count)
    sorted_display_names_count = utils.sort_dict_by_values(display_names_count)
    sorted_harmonized_names_count = utils.sort_dict_by_values(harmonized_names_count)
    sorted_all_names_count = utils.sort_dict_by_values(all_names_count)

    # Save the results to CSV
    utils.save_dict_to_csv(["attribute_name", "count"], sorted_attribute_names_count, OUTPUT_FILE_ATTRIBUTE_NAMES)
    utils.save_dict_to_csv(["display_name", "count"], sorted_display_names_count, OUTPUT_FILE_DISPLAY_NAMES)
    utils.save_dict_to_csv(["harmonized_name", "count"], sorted_harmonized_names_count, OUTPUT_FILE_HARMONIZED_NAMES)
    utils.save_dict_to_csv(["attribute_name|display_name|harmonized_name", "count"], sorted_all_names_count, OUTPUT_FILE_ALL_NAMES)

    print('Finished processing NCBI samples')
    print('- Total samples processed: ' + str(processed_samples_count))


if __name__ == "__main__":
    main()
