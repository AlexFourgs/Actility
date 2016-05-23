#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import sqlite3, os

class Database_Engine:
    # /home/alex/Documents/Cours/Stage Travaux/Actility/Programmes/DataBase/
    """
        This object is the database engine, his role is to :
            - Create the database if she doesn't exist
            - Add new data in the database
            - Remove data from the database
            - Edit data from the database
    """

    def __init__(self):
        if not os.path.exists("./DataBase/SensorsData.db"):
            self.create_database();
        else:
            self.db = sqlite3.connect("./DataBase/SensorsData.db")

    def create_database(self, sensors_dic={}):
        """
            This function create the database if she doesn't exist.
            She's executed only the first time you execute the software on a new machine.
            She creates the devices table and the data's table for each device.
        """
        self.db = sqlite3.connect("./DataBase/SensorsData.db")
        self.create_table("Device", ["Id CHAR(50) PRIMARY KEY","Model CHAR(50) NOT NULL"])

        if not sensors_dic:
            print("The sensor dictionnary is empty.")
        else:
            print("The sensor dictionnary isn't empty.")

    def create_table(self, table_name, list_data):
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
            print("Error, the data is already in the database.")


    def data_exist(self, table, key):
        request = "SELECT * FROM \'%s\' WHERE Id = \'%s\'"%(table, key)
        select = self.db.cursor()
        select.execute(request)
        rows = select.fetchall()

        if len(rows) == 0: # There is no columns with this primary key
            return True
        else:
            return False


    def record_exist(self, table, date):
        request = "SELECT * FROM \'%s\' WHERE Date = \'%s\'"%(table, date)
        select = self.db.cursor()
        select.execute(request)
        rows = select.fetchall()

        if len(rows) == 0: # There is no columns with this primary key
            return True
        else:
            return False

    def get_columns(self, table):
        columns = []

        for row in self.db.execute("pragma table_info('%s')"%(table)).fetchall():
            columns.append(row[1])

        columns.pop() # Remove the last element of the list which is the primary key column name
        return columns

    """
    def delete_table(self):
        # TODO

    def delete_data(self):
        # TODO

    def edit(self):
        # TODO

    def get_db(self):
        return self.db
    """

    def close_connection(self):
        self.db.close()

if __name__ == '__main__' :
    print("DATABASE MANAGER")

    database_engine = database_engine()
    database_engine.create_table("Device", ["Id CHAR(50) PRIMARY KEY","Model CHAR(50) NOT NULL"])
    database_engine.insert("Device", ["Id", "Model"], ["0018B20000000167", "Adeunis"])
    database_engine.close_connection()
