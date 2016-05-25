#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import client_engine, os, time, logging, logger_initializer
from bottle import route, run, request, response


def start_server():
    """Function that starts the server on port 8080"""
    run(host='0.0.0.0', port=8080)

@route("/", method="POST")
def listener():
    # curl -X POST --header "Content-Type:application/xml" --data @your_file.xml http://your_server.com:8080/
    #
    #print("Post receive from %s\n"%(ip))
    if(request.headers['Content-Type'] == "application/xml"):
        file_xml = request.body.read()
        file_path = engine.save_data_file(file_xml)
        engine.general_engine(file_path)
    else :
        logger = logging.getLogger("as_server")
        ip = request.environ.get('REMOTE_ADDR')
        print("Error, it's not a xml file\nFile rejected.\n")
        logger.warning("Class.Server :: listener :: HTTP POST REQUEST received from %s but body isn't a xml file. Rejected."%(ip))

if __name__ == '__main__':
    engine = client_engine.Engine()
    logger_initializer.init_log("as_server", "as_server.log")
    start_server()
