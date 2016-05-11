#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import client_engine, os
from bottle import route, run, request

class software:
    """
        This object is the software, he control everything :
            - listener
            - parser
            - decoder
            - database

        His role is to manage the data by the beginning (receive) to the end (save)
    """

    def __init__(self):
        self.engine = engine()


    @route("/listener", method="POST")
    def recolt_xml(self):
        if request.headers['Content-Type'] == "text/xml":
            file_xml = request.body.read()
            self.engine.save_data_file(file_xml)
            return "This is an xml file !\nXML FILE : " + file_xml
        else :
            return "Error, it's not a xml file\n"


if __name__ == '__main__':
    run(server='cherrypy', host='0.0.0.0', port=8080, debug=True)
