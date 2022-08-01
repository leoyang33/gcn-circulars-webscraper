""" GCN Circulars Look Up
This script scrapes NASA's GCN Archive and looks up circulars for given aliases
"""

import requests
import re

CIRCULAR_NUMBER_PATTERN = r"(NUMBER:  )(\d{5})"
CIRCULAR_SUBJECT_PATTERN = r"(SUBJECT: )(.*)"

def get_circulars(aliases):
    """Returns a dictionary mapping circular number to circular subject
    for all circulars associated with a given alias"""
    circulars = {}
    for alias in aliases:
        compiled_url = f"https://gcn.gsfc.nasa.gov/gcn/other/{alias}.gcn3"
        circulars_page = requests.get(compiled_url).text
        circular_numbers_matches = re.findall(
            CIRCULAR_NUMBER_PATTERN, circulars_page)
        circular_numbers = [x[1] for x in circular_numbers_matches]
        circular_subjects_matches = re.findall(
            CIRCULAR_SUBJECT_PATTERN, circulars_page)
        circular_subjects = [x[1] for x in circular_subjects_matches]
        for number, subject in zip(circular_numbers, circular_subjects):
            circulars[int(number)] = subject
    return circulars


def main():
    # Example input
    aliases = ["220715B"]
    results = get_circulars(aliases)
    print(results)


if __name__ == "__main__":
    main()
