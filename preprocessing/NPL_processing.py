import csv

import lxml.etree as ET
import os
import dateutil.parser
from csv import writer
import chardet


def newdom_to_list(newdom, year):
    r = newdom.__str__()
    resi = r.split("\t")
    result = []
    
    for double_string in resi:
        res = double_string.split("\n")
        result.append(res[0])
    result[0] = year
    return result


def all_entries_to_file(all_entries):
    with open('NPL_unprocessed.csv', "w", encoding="utf-8", newline="") as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(["", "text", "label", "date"])
    
    index = 0
    overall_index = 0
    for item in all_entries:
        with open('NPL_unprocessed.csv', "a", encoding="utf-8", newline="") as f:
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            year = item[0]
            item[0] = str(index)
            # writer.writerow(item)
            try:
                for line in item:
                    if str(line) == str(index):
                        continue
                    writer.writerow([str(overall_index), line, year])
                    overall_index += 1
            except UnicodeEncodeError:
                print("what the f", index, line)
                str.encode(line, encoding="utf-8")
                pass
        index += 1
        #print(index)


xml_per_year = {1998: 58, 1999: 201, 2000: 183, 2001: 181, 2002: 186, 2003: 188, 2004: 180, 2005: 167, 2006: 168,
                2007: 179, 2008: 176, 2009: 151, 2010: 106,
                2011: 108, 2012: 103, 2013: 99, 2014: 91, 2015: 98, 2016: 100, 2017: 99, 2018: 98, 2019: 98, 2020: 104,
                2021: 98, 2022: 46}

inputpath = "ParlaMint-NO"

xml_filename = "NPL.xml"
xsl_filename = "parlamint-tei2text.xsl"

import datefinder

start_year = 1998
end_year = 2022
current_year = start_year

import glob
from chardet.universaldetector import UniversalDetector
with open(xml_filename, 'rb') as f:
    enc = chardet.detect(f.read())
    print(enc)
    
    
all_entries = []
xslt = ET.parse(xsl_filename)
print(xslt.docinfo.encoding)
transform = ET.XSLT(xslt)

all_entries = (newdom_to_list(transform(ET.parse(f"{inputpath}/{year}/{filename}")), year)
               for year in range(start_year, end_year + 1)
               for dirpath, dirnames, filenames in os.walk(f"{inputpath}/{year}")
               for filename in filenames if filename.endswith('.xml') and xml_per_year[year] > 0
               if xml_per_year.__setitem__(year, xml_per_year[year] - 1) or True)

all_entries_to_file(all_entries)
