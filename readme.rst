======
README
======

===================
Applications Server
===================

Created by Alexandre Fourgs
---------------------------

:Version: 1.0
:Python version: 2.7
:Description: This is a document for helping install and use the program.
:Source: <http://github.com/AlexFourgs/Actility>


Requirements
------------

================  ============================================================
API / Libraries   Version
================  ============================================================
Python            2.6
Bottlepy          0.12.9
lxml              3.3.3.0
SQLite3           3.8.2
================  ============================================================


How to install them
-------------------

1) With pip tool
    i) Open a terminal and go into the folder Actility/Documentations.
    ii) Enter "pip install -r requirements.txt" and all libraries will be installed.


2) With the script shell
    i) Open a terminal and go into the folder Actility/Documentations.
    ii) Enter "sh install.sh" or "bash install.sh" and all libraries will be installed.


**If you choose to install the requirements by your own way, the creator of this project isn't responsible of the eventual bug that you will have.**


How to use it
-------------

In a terminal, go into the folder "**Actility**" of the project and enter "**python Programs/application_server.py**"

Then your server is started, A web page is locally accessible to display the data collected in the form of graphs at this url : <http://localhost:8080/data>
