import time
import sys
import os
import xml.dom.pulldom as pulldom
import gzip
import csv
import re
from itertools import permutations


def get_base_folder(expected_exec_folder):
    """
    Returns the right execution folder
    :param expected_exec_folder:
    :return:
    """
    import os
    current_exec_folder = os.path.split(os.getcwd())[1]
    if current_exec_folder == expected_exec_folder:
        return '.'
    elif current_exec_folder != expected_exec_folder and current_exec_folder == 'scripts':
        return './..'
    elif current_exec_folder != expected_exec_folder and current_exec_folder == 'test':
        return './../..'
    else:
        print("Error: Cannot figure out the right execution folder\n")
        sys.exit(1)


def log_progress(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    # slow down the rate at which the messages are printed
    if count % 1000 == 0 or percent == 100:
        sys.stdout.write("...%d%%, %d MB, %d KB/s, %d seconds passed\r" %
                         (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def confirm(question):
    # raw_input returns the empty string for "enter"
    yes = {'yes', 'y'}
    no = {'no', 'n'}
    sys.stdout.write(question)
    choice = input().lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        sys.stdout.write("Please respond 'y' or 'n'")


def save_dict_to_csv(headers, dct, output_file_path):
    """
    Saves a dictionary to a CSV file
    :param headers: array with headers (e.g., ["Attribute name", "Count"]
    :param dct: input dictionary
    :param output_file_path:
    :return:
    """
    import csv
    import os

    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))
    f = csv.writer(open(output_file_path, "w"))
    if headers is not None:
        f.writerow(headers)
    for key, val in dct.items():
        f.writerow([key, val])


def save_json_to_csv(input_json, output_file_path):
    """
    Saves an array of json objects to CSV
    :param input_json:
    :param output_file_path:
    :return:
    """

    # Save headers
    headers = []
    for key in input_json[0]:
        headers.append(key)

    f = csv.writer(open(output_file_path, "w"))
    f.writerow(headers)

    # Iterate through each record in the JSON Array
    for record in input_json:
        # Create placeholder to hold the data for the current record
        current_record = []
        # Iterate through each key in the keylist and add the data to our current record list
        for key in headers:
            current_record.append(record[key])
            # Write the current record as a line in our CSV
        f.writerow(current_record)


def sort_dict_by_values(dct):
    """
    Sorts a dictionary by its values
    :param dct:
    :return: a dictionary ordered by key values
    """
    import collections
    sorted_dct = {k: v for k, v in sorted(dct.items(), key=lambda item: item[1], reverse=True)}
    return collections.OrderedDict(sorted_dct)


def camel_case_to_space_delimited(term):
    return re.sub("([a-z])([A-Z])", "\g<1> \g<2>", term)
    # matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', term)
    # return [m.group(0) for m in matches]


def norm_str(input_str):
    """
    Normalizes a string by applying the following transformations:
    1) Remove special characters
    2) Replace multiple blanks by one
    3) Remove leading and trailing whitespaces
    4) Transform to uppercase
    :param input_str: input string
    :return: normalized string
    """
    import re
    if input_str is not None:
        input_str = re.sub('[^A-Za-z0-9]+', ' ', input_str)
        input_str = re.sub(' +', ' ', input_str)
        return input_str.strip().upper();
    else:
        return None


def equal_norm_str(str1, str2):
    """
    Checks if two normalized strings are equal
    :param str1:
    :param str2:
    :return: True if the normalized strings are equal. False otherwise
    """
    if norm_str(str1) == norm_str(str2):
        return True
    else:
        return False


# def ends_with_norm_str(str1, str2):
#     """
#     Checks if a normalized string str1 ends with a normalized string str2. The goal is to identify subtypes of a term
#     (e.g., MALIGNANTHEPATOMA ends with HEPATOMA => malignant hepatoma is a subtype of hepatoma
#     :param str1:
#     :param str2:
#     :return:
#     """
#     if norm_str(str1).endswith(norm_str(str2)):
#         return True;
#     else:
#         return False;


def contained_in_list_norm_str(str, str_list):
    """
    Checks if a string is contained in a list of strings. The comparisons are done using normalized strings
    :return: boolean
    """
    if str is None or len(str) == 0 or str_list is None or len(str_list) == 0:
        return False;
    else:
        str_norm = norm_str(str)
        list_norm = [norm_str(item) for item in str_list]
        if str_norm in list_norm:
            return True
        else:
            return False


def generate_str_permutations(term):
    """
    Generates all permutations of words in a multi-word terms. The result includes the original string. 
    Example: "hepatocellular carcinoma" -> ["hepatocellular carcinoma", "carcinoma hepatocellular"]. It also performs
    basic normalization
    :param str:
    :return: list of permutations
    """
    result = []

    term = re.sub('[^A-Za-z0-9]+', ' ', term)
    term = re.sub(' +', ' ', term)
    term = term.strip()

    terms = term.split()
    if len(terms) <= 1:
        result.append(term)
    else:
        for perm in permutations(terms, len(terms)):
            result.append(" ".join(perm))

    return result


def read_xml_or_gz_file(input_file_path):
    """
    Reads a file in xml format and returns its content. If the file is zipped, it unzips it first
    :param input_file_path:
    :return:
    """
    input_file_extension = os.path.splitext(input_file_path)[1]
    # Read biosamples from XML file
    if input_file_extension == '.gz':
        content = pulldom.parse(gzip.open(input_file_path))
    elif input_file_extension == '.xml':
        content = pulldom.parse(input_file_path)
    else:
        print('Error: invalid file extension')
        sys.exit(1)
    return content


def add_timestamp_to_filename(file_path):
    """
    Prepends timestamp
    :return:
    """
    import time
    base_path = file_path.rsplit('/', 1)[0]
    file_name = file_path.rsplit('/', 1)[1]
    return str(base_path) + '/' + str(time.strftime("%Y%m%d-%H%M%S_")) + str(file_name)


# if __name__ == "__main__":
#     print(norm_str("  hepatoceLLular, carcinoma    (Malignant)  "))
#     print(norm_str("  (female:) bla  "))
#     print(contained_in_list_norm_str("  (HCC) ", ["_Hcc,"]))
#     print(generate_str_permutations("HCC"))
#     print(generate_str_permutations("malignant hepatocellular carcinoma"))
