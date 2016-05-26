#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import sqlite3, os, logging, logger_initializer
from logging import handlers

class DatabaseEngine:
    # /home/alex/Documents/Cours/Stage Travaux/Actility/Programmes/DataBase/
    """
        This object is the database engine, his role is to :
            - Create the database if she doesn't exist
            - Add new data in the database
            - Remove data from the database
            - Edit data from the database
    """

    def __init__(self):
        #self.logger = logger_initializer.init_log("as_database", "as_database.log")
        if not os.path.exists("./DataBase/SensorsData.db"):
            self.create_database();
        else:
            self.db = sqlite3.connect("./DataBase/SensorsData.db")

    def create_database(self, sensors_dic={}):
        """
            This method creates the database if she doesn't exist.
            She's executed only the first time you execute the software on a new machine.
            She creates the devices table and the data's table for each device.
        """
        self.db = sqlite3.connect("./DataBase/SensorsData.db")
        self.create_table("Device", ["Id CHAR(50) PRIMARY KEY","Model CHAR(50) NOT NULL"])

        if not sensors_dic:
            #self.logger.warning("Class.DatabaseEngine :: create_database :: sensors_dic object is empty.")
            print("Error")

    def create_table(self, table_name, list_data):
        """Method that creates a new table if she doesn't exist."""
        request = "CREATE TABLE IF NOT EXISTS %s (" %(table_name)
        i = 0
        while i < len(list_data):
            if i != len(list_data)-1:
                request = request + list_data[i] + ", "
            else :
                request = request + list_data[i] + ");"
            i+=1

        self.db.execute(request)
        self.db.commit()

    def insert(self, table_name, list_value_to_add, list_value_data):
        """Method that add a new line into a table"""
        exist = "SELECT * FROM %s WHERE \'Date\'=\'%s\'"%(table_name, list_value_data[0])
        select = self.db.cursor()
        select.execute(exist)
        rows = select.fetchall()

        if len(rows) == 0:
            request = "INSERT INTO %s (" %(table_name)

            i=0
            while i < len(list_value_to_add) :
                if i != len(list_value_to_add)-1 :
                    request = request + list_value_to_add[i] + ", "
                else :
                    request = request + list_value_to_add[i] + ") VALUES ("
                i+=1

            i=0
            while i < len(list_value_data) :
                if i != len(list_value_data)-1 :
                    if isinstance(list_value_data[i], str):
                        request = request + "'" + list_value_data[i] + "', "
                    else :
                        request = request + str(list_value_data[i]) + ", "
                else :
                    if isinstance(list_value_data[i], str):
                        request = request + "'" + list_value_data[i] + "')"
                    else :
                        request = request + str(list_value_data[i]) + ")"
                i+=1

            print(request)
            self.db.execute(request)
            self.db.commit()

        else:
            #self.logger.warning("Class.DatabaseEngine :: insert :: Try to add a value already in the database.")
            print("Error")

    def data_exist(self, table, key):
        """Method that returns if the data exist by comparing the IDs"""
        request = "SELECT * FROM \'%s\' WHERE Id = \'%s\'"%(table, key)
        select = self.db.cursor()
        select.execute(request)
        rows = select.fetchall()

        if len(rows) == 0: # There is no columns with this primary key
            return True
        else:
            return False

    def record_exist(self, table, date):
        """Method that returns if the record in the table exist by comparing the dates"""
        request = "SELECT * FROM \'%s\' WHERE Date = \'%s\'"%(table, date)
        select = self.db.cursor()
        select.execute(request)
        rows = select.fetchall()

        if len(rows) == 0: # There is no columns with this primary key
            return True
        else:
            return False

    def get_columns(self, table):
        """Methods that return all columns name from the table"""
        columns = []

        for row in self.db.execute("pragma table_info('%s')"%(table)).fetchall():
            columns.append(row[1])

        columns.pop() # Remove the last element of the list which is the primary key column name
        return columns


#    def delete_table(self):
#        # TODO
#
#    def delete_data(self):
#        # TODO
#
#    def edit(self):
#        # TODO
#
#    def get_db(self):
#        return self.db

    def close_connection(self):
        self.db.close()

if __name__ == '__main__' :
    print("DATABASE MANAGER")

    database_engine = DatabaseEngine()
    database_engine.create_table("Device", ["Id CHAR(50) PRIMARY KEY","Model CHAR(50) NOT NULL"])
    database_engine.insert("Device", ["Id", "Model"], ["0018B20000000167", "Adeunis"])
    database_engine.close_connection()
