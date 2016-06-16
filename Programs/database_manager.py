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

            #print(request)
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

    def get_id_model(self, model):
        """Method for get all id registered in the database for the model specified"""
        list_id = []
        request = "SELECT Id FROM Device WHERE Model = \'%s\'"%(model)

        select = self.db.cursor()
        select.execute(request)
        ids = select.fetchall()

        for actual in ids:
            list_id.append(actual[0])

        return list_id

    def data_for_graph(self, model, device_id, data, date_from, date_to):
        """Methods that executes a SELECT request and returns the results formated in JSON"""
        request_data = "SELECT " + data +", Date, DeviceId FROM "+model+" WHERE DeviceId=\""+device_id+"\" AND Date >= \""+ date_from +"\" AND Date <= \""+date_to+"\" ORDER BY Date"
        select = self.db.cursor()
        select.execute(request_data)
        all_data = select.fetchall()

        return all_data # With [2]=ID model [1]=Date [0]=Value

    def get_columns(self, table):
        """Methods that return all columns name from the table"""
        columns = []

        for row in self.db.execute("pragma table_info('%s')"%(table)).fetchall():
            columns.append(row[1])

        columns.pop() # Remove the last element of the list which is the primary key column name
        return columns

    def get_columns_data(self, table):
        columns = self.get_columns(table)
        columns.pop() # Delete column device_id
        columns.pop() # Delete column Date

        return columns

    def get_device_model(self, device_id):
        """Methods that returns the model of the device by comparing ID"""
        request = "SELECT Model FROM Device WHERE Id = \'%s\'"%(device_id)
        #print(request)

        select = self.db.cursor()
        select.execute(request)
        model = select.fetchone()

        if model==None: # Device isn't in the database
            return False
        else :
            return model[0]

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
    #database_engine.create_table("Device", ["Id CHAR(50) PRIMARY KEY","Model CHAR(50) NOT NULL"])
    #database_engine.insert("Device", ["Id", "Model"], ["0018B20000000167", "Adeunis"])

    model = database_engine.get_device_model("0028B20000000167")
    print(model)

    database_engine.get_id_model("Adeunis")
    database_engine.get_id_model("Watteco")


    columns = database_engine.get_columns_data("Adeunis")
    for column in columns:
        print column

    columns = database_engine.get_columns_data("Watteco")
    for column in columns:
        print column

    database_engine.data_jsons("Adeunis", "0018B20000000167", "Temperature", "2016-05-24 11:41:48", "2016-05-26 14:42:17")

    database_engine.close_connection()
