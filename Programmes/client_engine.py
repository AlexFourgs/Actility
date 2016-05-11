#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import database_manager
from lxml import etree
from datetime import datetime

class engine:
    """
        This object is the engine of the software that gathering data from http request post.
        His role is to :
            - generate the database if she was not created
            - parse the .xml file
            - decrypt the payload
            - create the corresponding objects
            - add data to the sql database
    """

    def __init__(self):
        self.__sensors_db = sensors()
        self.__database_engine = database_manager.database_engine()

    def parse_xml(self, file):
        # TODO écrire cette fonction
        pass

    def watteco_decoder(self, data):
        """Function that decode the hex data from a Watteco 3.1 sensor"""
        lenght_data = len(data)

        if lenght_data != 114 :
            return "Error, payload size is not correct."
        else :
            # On décode le payload
            version = int(data[0])
            payload_len = int(data[10:12], 16)
            nexthdr = data[12:14]
            hop_limit = int(data[14:16], 16)
            saddr = data[16:48]
            daddr = data[48:80]
            udp_port_source = int(data[80:84], 16)
            udp_port_dest = int(data[84:88], 16)
            lenght_udp = int(data[88:92], 16)
            checksum = data[92:96]
            raw_payload = data[96:114]
            mesured_value = (float(int(data[110:114], 16)))/100

            # On créer la liste des données enregistrés et on la renvoi.
            new_data = raw_data("Temperature", mesured_value)
            list_recorded_data=[new_data]

            return list_recorded_data

    def adeunis_lorawan_demonstrator_decoder(self, data):
        """Function that decode the hex data from an Adeunis LoRaWan Demonstrator sensor"""

        lenght_data = len(data)

        if lenght_data == 12 : # Only temperature
            temp = float(int(data[2:4], 16))
            uplink_counter = int(data[4:6], 16)
            downlink_counter = int(data[6:8], 16)
            battery = float(int(data[8:12], 16))/1000
            latitude = 0
            longitude = 0

            new_data = raw_data("Temperature", temp)
            new_data_2 = raw_data("Latitude", latitude)
            new_data_3 = raw_data("Longitude", longitude)

            list_recorded_data=[new_data, new_data_2, new_data_3]

            return list_recorded_data


        elif lenght_data == 28 : # Temperature + GPS
            temp = int(data[2:4], 16)
            latitude = data[4:12]
            longitude = data[12:20]
            uplink_counter = int(data[20:22], 16)
            downlink_counter = int(data[22:24], 16)
            battery= float(int(data[24:28], 16))/1000

            new_data = raw_data("Temperature", temp)
            new_data_2 = raw_data("Latitude", latitude)
            new_data_3 = raw_data("Longitude", longitude)

            list_recorded_data=[new_data, new_data_2, new_data_3]

            return list_recorded_data

        else :
            return "Error, payload size is not correct."

        # TODO : Créer l'objet et l'ajouter à la DB

    def new_device(self, name, device_id):
        """ This function create and add a new sensor to the database sensors object """

        if self.__sensors_db.get_devices().has_key(device_id):
            print "Device [%s] %s already in the database" %(device_id, name)
        else:
            new_sensor = sensor_device(name, device_id)
            self.__sensors_db.add_device(new_sensor)

        self.__database_engine.insert("Device", ["Id", "Model"], [device_id, name])

    def decode_and_add_record(self, device_id, date, data):
        name_device = self.__sensors_db.get_devices()[device_id].get_name()

        if name_device == "Watteco":
            list_recorded_data = self.watteco_decoder(data)
            new_record = record_data(date, list_recorded_data)
            self.__sensors_db.get_devices()[device_id].add_data(new_record)
            self.__database_engine.insert("Watteco", ["DeviceId", "Date", "Temperature"], [device_id ,date.strftime('%Y-%m-%d %H:%M:%S'), list_recorded_data[0].get_value()])

        elif name_device == "Adeunis" :
            list_recorded_data = self.adeunis_lorawan_demonstrator_decoder(data)
            new_record = record_data(date, list_recorded_data)
            self.__sensors_db.get_devices()[device_id].add_data(new_record)
            self.__database_engine.insert("Adeunis", ["DeviceId", "Date", "Temperature", "Latitude", "Longitude"], [device_id, date.strftime('%Y-%m-%d %H:%M:%S'), list_recorded_data[0].get_value(), list_recorded_data[1].get_value(), list_recorded_data[2].get_value()])

    def get_sensors_db(self):
        return self.__sensors_db

    def close_database_connection(self):
        self.__database_engine.close_connection()

    def save_data_file(self, xml_file=""):
        """ This function create a xml file with the DATA from the POST method and save it into the path DATA """

        # We take the date for named the new xml file.
        date = time.localtime()
        file_name = "./DATA/" + str(date.tm_mday) + "_" + str(date.tm_mon) + "_" + str(date.tm_year) + "_" + str(date.tm_hour) + "_" + str(date.tm_min) + "_" + str(date.tm_sec)

        with open(file_name, "w") as new_xml_file:
            new_xml_file.write(xml_file)

        new_xml_file.close()


class sensors:
    """
        This is a little database with the list of all sensor device objects.
    """

    def __init__(self):
        self.devices = {}

    def add_device(self, device):
        """ Add a new device into the dictionnary devices """
        # On vérifie lorsqu'on ajoute un device au dictionnaire que c'est bien un objet de type "sensor_device"
        # La clé du dictionnaire est l'ID du device car unique et propre à chaque devices.
        if isinstance(device, sensor_device):
            self.devices[device.get_device_id()] = device
        else:
            return "Error while adding the device object into devices.\n device type : %s\nWaiting an object [SENSOR_DEVICE]\n" %(type(device))

    def add_data(self, data, device_id):
        # On vérifie lorsqu'on ajoute l'objet data à la liste que c'est bien un objet de type "record_data"
        if isinstance(data, record_data):
            self.devices[device_id].add_data(data)
        else:
            return "Error while adding the data object into data_list.\n data type : %s\nWaiting an object [RECORD_DATA]\n" %(type(data))

    def get_devices(self):
        """ Return the dictionnary of the devices as values and the IDs as keys """
        return self.devices

    def __str__(self):
        list_str = "List of all devices :\n\n"
        for device_id in self.devices.keys():
            list_str = list_str + self.devices[device_id].get_name_and_id()

        return list_str


class sensor_device:
    """
        It's an object that contains information about a particular sensor :
            - Device's ID.
            - Device's name (Watteco or Adeunis for example).
            - all recorded data from a sensor_device.
    """

    def __init__(self, name, device_id):
        self.__name = name
        self.__device_id = device_id
        self.__data_list = [] # List of object "record_data"

    def add_data(self, data):
        """ Add a new data to the recorded list data from the device """
        # On vérifie lorsqu'on ajoute l'objet data à la liste que c'est bien un objet de type "record_data"
        if isinstance(data, record_data):
            self.__data_list.append(data)
        else:
            return "Error while adding the data object into data_list.\n data type : %s\nWaiting an object [RECORD_DATA]\n" %(type(data))


    def number_of_registered_data(self):
        """ Print the number of recorded data from the device """
        return "Number of registered data : %s" %(len(self.__data_list))

    def list_all_data(self):
        """ Print all recorded data from the device """
        for actual_recorded_data in self.__data_list :
            print(actual_recorded_data)

    def get_device_id(self):
        """ Return the device's id """
        return self.__device_id

    def get_name(self):
        """ Return the device's model """
        return self.__name

    def get_name_and_id(self):
        """ A simple function that return a string with the name and the ID """
        return "Name : %s, ID : %s\n" %(self.__name, self.__device_id)


class record_data:
    """
        It's an object that represents a record from a sensor.
        It is specified by the date of the record and a list of the data recorded by the sensor.
    """

    def __init__(self, date, data_list):
        self.date = date
        # On vérifie que data_list est bien une liste.
        if isinstance(data_list, list):
                self.data_list = data_list # List of object "raw_data"
        else:
            return "Error while creating the record_data object.\n data_list type : %s\nWaiting an object [LIST]\n" %(type(data_list))


    def get_date(self):
        return self.date

    def get_data_list(self):
        return self.data_list

    def __str__(self):
        string = "Date : %s\nData :\n" %(self.date)
        for actual_data in self.data_list :
            string = string + actual_data.get_data()

        return string


class raw_data:
    """
        It's an object that represents a data by his type and his value.
        For example :
            Type : Temperature, Value : 34
    """

    def __init__(self, data_type, value):
        self.data_type = data_type
        self.value = value

    def get_value(self):
        return self.value

    def get_data(self):
        return "Type : %10s\tValue : %10s\n" %(self.data_type, self.value)



if __name__ == '__main__':
    engine = engine()

    ## Test d'ajout de device.
    ## OK POV object
    ## OK POV database
    engine.new_device("Adeunis", "0018B20000000167")
    engine.new_device("Adeunis", "0018B20000000167")
    engine.new_device("Watteco", "70B3D5E75E000239")
    device_db_object = engine.get_sensors_db()

    ## Tests des fonctions de décodage de payload et d'ajout dans les objets.
    ## OK POV object
    ## OK POV database
    engine.decode_and_add_record("0018B20000000167", datetime(2016, 1, 1, 0, 0, 0), "8e3036840b05")
    engine.decode_and_add_record("0018B20000000167", datetime(2016, 1, 1, 0, 0, 0), "9e31485592200021746034830b1c")
    engine.decode_and_add_record("70B3D5E75E000239", datetime(2016, 1, 1, 0, 0, 0), "6000000000111140000000000000000070b3d5e75e0002390000000000000000000000ff00000000f0b5f0b400111b79110a0402000029091d")

    engine.close_database_connection()
