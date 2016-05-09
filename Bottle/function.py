#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import time, os

def save_data(xml_file=""):
    """ This function create a xml file with the DATA from the POST method and save it into the path DATA """

    # We take the date for named the new xml file.
    date = time.localtime()
    file_name = "./DATA/" + str(date.tm_mday) + "_" + str(date.tm_mon) + "_" + str(date.tm_year) + "_" + str(date.tm_hour) + "_" + str(date.tm_min) + "_" + str(date.tm_sec)

    with open(file_name, "w") as new_xml_file:
        new_xml_file.write(xml_file)

    new_xml_file.close()
