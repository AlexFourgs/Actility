#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import client_engine, os, time, logging
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
        self.logger = self.init_log()
        self.engine = client_engine.Engine()
        self.app = Bottle()

    def init_log(self):
        """Initialise the server logger and return it."""
        logger = logging.getLogger("as_server")
        log_format = logging.Formatter("[%(asctime)s] %(levelname)s :: %(message)s")
        handler_server = logging.FileHandler("/var/log/as_server.log", mode="a", encoding="utf-8") # Only work for linux system
        handler_server.setFormatter(log_format)
        handler_server.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler_server)

        return logger

    def route(self):
        self.app.route("/", method="POST", callback=self.listener)

    def start(self):
        """Method that starts the server on port 8080"""
        self.app.run(host='0.0.0.0', port=8080)

    def listener(self):
        # curl -X POST --header "Content-Type:application/xml" --data @your_file.xml http://your_server.com:8080/
        #
        #print("Post receive from %s\n"%(ip))
        if(request.headers['Content-Type'] == "application/xml"):
            file_xml = request.body.read()
            file_path = engine.save_data_file(file_xml)
            engine.general_engine(file_path)
        else :
            ip = request.environ.get('REMOTE_ADDR')
            print("Error, it's not a xml file\nFile rejected.\n")
            self.logger.warning("Class.Server :: listener :: HTTP POST REQUEST received from %s but body isn't a xml file. Rejected."%(ip))
            #TODO: Write it into log file


if __name__ == '__main__':
    server = Server()
    server.start()
