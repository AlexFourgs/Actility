#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import client_engine, os
from bottle import route, run, request

"""class software:
    """"""
        This object is the software, he control everything :
            - listener
            - parser
            - decoder
            - database

        His role is to manage the data by the beginning (receive) to the end (save)
    """"""

    def __init__(self):
        self.engine = engine()


    @route("/listener", method="POST")
    def recolt_xml(self):
        if request.headers['Content-Type'] == "text/xml":
            file_xml = request.body.read()
            self.engine.save_data_file(file_xml)
            #return "This is an xml file !\nXML FILE : " + file_xml
        else :

            #return "Error, it's not a xml file\n"
"""
def save_data_file(self, xml_file=""):
    """ This function create a xml file with the DATA from the POST method and save it into the path DATA """

    # We take the date for named the new xml file.
    date = time.localtime()
    file_name = "./DATA/" + str(date.tm_mday) + "_" + str(date.tm_mon) + "_" + str(date.tm_year) + "_" + str(date.tm_hour) + "_" + str(date.tm_min) + "_" + str(date.tm_sec)

    with open(file_name, "w") as new_xml_file:
        new_xml_file.write(xml_file)

    new_xml_file.close()


# Permet de récupérer les fichiers XML via protocole HTTP "POST" et affiche le contenu du fichier.
# curl -X POST --header "Content-Type:text/xml;charset=UTF-8" --data @test_xml.xml http://192.168.1.20:8080/listener
@route("/listener", method="POST")
def recolt_xml():
    if request.headers['Content-Type'] == "text/xml":
        file_xml = request.body.read()
        save_data_file(file_xml)
        print "This is an xml file !\nXML FILE : " + file_xml
    else :
        print "Error, it's not a xml file\n"


#run(server='cherrypy', host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    #run(server='cherrypy', host='0.0.0.0', port=8080, debug=True)
    run(host='0.0.0.0', port=8080, debug=True)
