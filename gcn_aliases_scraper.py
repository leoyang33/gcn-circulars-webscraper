<<<<<<< HEAD
"""GCN Event Name Lookup
=======
""" NASA GCN Archive Scraper
>>>>>>> ec34b33b03cc39a375e6026880e459b45125fe59
This script scrapes NASA's GCN Archive and looks up aliases for an event

Requires "BeautifulSoup4" library
"""

import requests
from bs4 import BeautifulSoup
import re

CIRCULARS_URL = "https://gcn.gsfc.nasa.gov/gcn/selected.html"


def get_aliases(dateobs):
    """Returns a list of aliases for a GCN event

    Parameters
    ----------
    dateobs : str
        The originally observed date of the event

    Returns
    -------
    array
        An array of strings that are aliases for the event
    """
    split_date = dateobs.split("T", 1)
    date = split_date[0].replace("-", "")[2:]
    time = split_date[1]
    date_pattern = f".*{date}.*"

    all_circulars_page = requests.get(CIRCULARS_URL)
    all_circulars_soup = BeautifulSoup(
        all_circulars_page.content, "html.parser")
    date_matches = all_circulars_soup.find_all(
        "b", text=re.compile(date_pattern))
    new_gcn_aliases = []

    if date_matches:
        for date_match in date_matches:
            print(date_match.text)
            formatted_name = date_match.text.replace("_"," ").replace("-"," ").split()[1][:-1]
            compiled_url = f"https://gcn.gsfc.nasa.gov/gcn/other/{formatted_name}.gcn3"
            circulars_page = requests.get(compiled_url)
            if time in circulars_page.text:
                new_gcn_aliases.append(formatted_name)
                break
    return new_gcn_aliases


def main():
    # Example input
    dateobs = "2022-07-28T16:20:39"
    results = get_aliases(dateobs)
    print(results)


if __name__ == "__main__":
    main()
