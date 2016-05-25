#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import client_engine, os, time
from bottle import Bottle, route, run, request, response

class Server:
    """
        This object is the server, he control everything :
            - listener
            - parser
            - decoder
            - database

        His role is to manage the data by the beginning (receive) to the end (save)
    """

    def __init__(self):
        self.engine = client_engine.Engine()
        self.app = Bottle()

    def route(self):
        self.app.route("/", method="POST", callback=self.listener)

    def start(self):
        self.app.run(host='0.0.0.0', port=8080)

    def listener(self):
        # curl -X POST --header "Content-Type:application/xml" --data @your_file.xml http://your_server.com:8080/
        #ip = request.environ.get('REMOTE_ADDR')
        #print("Post receive from %s\n"%(ip))
        if(request.headers['Content-Type'] == "application/xml"):
            file_xml = request.body.read()
            file_path = engine.save_data_file(file_xml)
            engine.general_engine(file_path)
        else :
            print("Error, it's not a xml file\nFile rejected.\n")
            #TODO: Write it into log file


if __name__ == '__main__':
    #run(host='0.0.0.0', port=8080, debug=True)
    server = Server()
    server.start()
