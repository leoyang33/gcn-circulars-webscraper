# This file scrapes NASA's GCN Archive and organizes the data in a csv

import requests
from bs4 import BeautifulSoup
import csv
import re

URL = "https://gcn.gsfc.nasa.gov/gcn/selected.html"
SPLITTER = "////////////////////////////////////////////////////////////////////////"
PATTERN = r"(?<!\d)(NUMBER:  )\d{5}(?!\d)"
FERMI_DATE_PATTERN = r"(?<!\d)(At )\d{2}(:)\d{2}(:)\d{2}(.\d{2,3})?( UT on )\d{1,2}( [a-zA-Z]{3,10} )\d{4}(?!\d)" #and CALET
SWIFT_DATE_PATTERN = r"(?<!\d)(At )\d{2}(:)\d{2}(:)\d{2}( UT, the Swift)(?!\d)"
ICECUBE_DATE_PATTERN = r"(?<!\d)(On )\d{2}(\/)\d{2}(\/)\d{2}( at )\d{2}(:)\d{2}(:)\d{2}(?!\d)"
GRB_PATTERN = r"(?<!\d)(GRB )\d{6}[A-Z](?!\d)" # For date extraction
MONTH_TO_NUM = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
    'March': '03',
    'June': '06',
    'July': '07',
    'April': '04'
}

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
li = soup.find("dl").find_all("dt")

with open("circulars2.csv", "w+", encoding="utf-8") as f:
    writer = csv.writer(f)
    # String, String, List
    writer.writerow(["Event", "Link", "Circulars", "DateObs"])
    line = 0
    for i in li:
        print(line)
        line+=1
        # EVENT NAME
        name = i.find('b').text[:-1]
        # EVENT LINK
        a = i.find('a', href=True)
        link = f"https://gcn.gsfc.nasa.gov/gcn/{a['href']}"
        # INDIVIDUAL CIRCULARS
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        circulars = []
        for match in re.finditer(PATTERN, soup.text):
            s = match.group(0).split()
            circulars.append(int(s[1]))
        # DATE
        # fermi, CALET
        if re.search(FERMI_DATE_PATTERN, soup.text):
            match = re.search(FERMI_DATE_PATTERN, soup.text)
            s = match.group(0).split()
            date = f"{s[6][2:]}{MONTH_TO_NUM[s[5]]}{s[4]} {s[1].split('.')[0]}"
        # swift
        elif re.search(SWIFT_DATE_PATTERN, soup.text) and re.search(GRB_PATTERN, soup.text):
            match = re.search(SWIFT_DATE_PATTERN, soup.text)
            s = match.group(0).split()
            day = re.search(GRB_PATTERN, soup.text)
            d = day.group(0).split()
            date = f"{d[1][:-1]} {s[1]}"
        # icecube
        elif re.search(ICECUBE_DATE_PATTERN, soup.text):
            match = re.search(ICECUBE_DATE_PATTERN, soup.text)
            s = match.group(0).split()
            date = f"{s[1].replace('/','')} {s[3]}"
        else:
            date = "No date found"

        writer.writerow([name, link, circulars, date])
