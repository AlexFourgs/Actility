#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import database_manager, logging, logger_initializer
from lxml import etree
from datetime import datetime
import time
from io import StringIO

class RawData:
    """
        It's an object that represents a data by his type and his value.
        For example :
            Type : Temperature, Value : 34
    """

    def __init__(self, data_type, value):
        self.data_type = data_type
        self.value = value

    def get_value(self):
        """Return the value of the data"""
        return self.value

    def get_data(self):
        """Return a string that specifies the data type and value"""
        return "Type : %10s\tValue : %10s\n" %(self.data_type, self.value)


class RecordData:
    """
        It's an object that represents a record from a sensor.
        It is specified by the date of the record and a list of the data recorded by the sensor.
    """

    def __init__(self, date, data_list):
        self.logger = logger_initializer.init_log("as_engine", "as_engine.log")
        self.date = date
        # Verifying that "data_list" is a list .
        if isinstance(data_list, list):
                self.data_list = data_list # List of object "RawData"
        else:
            self.logger.warning("Class.RecordData :: __init__ :: Error while creating the RecordData object. data_list type : [%s] Waiting an object [LIST]" %(type(data_list)))

    def get_date(self):
        """Return the record date"""
        return self.date

    def get_data_list(self):
        """Return the record list of data"""
        return self.data_list

    def __str__(self):
        """Return a string of the record date and data"""
        string = "Date : %s\nData :\n" %(self.date)
        for actual_data in self.data_list :
            string = string + actual_data.get_data()

        return string


class SensorDevice:
    """
        It's an object that contains information about a particular sensor :
            - Device's ID.
            - Device's model (Watteco or Adeunis for example).
            - all recorded data from a sensor_device.
    """

    def __init__(self, model, device_id):
        self.logger = logger_initializer.init_log("as_engine", "as_engine.log")
        self.__model = model
        self.__device_id = device_id
        self.__data_list = [] # List of object "RecordData"

    def add_data(self, data):
        """ Add a new data to the recorded list data from the device """
        # Verifying type of data.
        if isinstance(data, RecordData):
            self.__data_list.append(data)
        else:
            self.logger.warning("Class.SensorDevice :: add_data :: Error while adding the data object into data_list. Data type : [%s] Waiting an object [RecordData]" %(type(data)))

    def number_of_registered_data(self):
        """ Return a string with the number of recorded data from the device """
        return "Number of registered data : %s" %(len(self.__data_list))

    def list_all_data(self):
        """ Method that show a message with all recorded data from the device """
        for actual_recorded_data in self.__data_list :
            print(actual_recorded_data)

    def get_device_id(self):
        """ Return the device's id """
        return self.__device_id

    def get_model(self):
        """ Return the device's model """
        return self.__model

    def get_model_and_id(self):
        """ A simple method that return a string with the model and the ID """
        return "model : %s, ID : %s\n" %(self.__model, self.__device_id)


class Sensors:
    """
        This is a little database object oriented with the list of all sensor device objects.
    """

    def __init__(self):
        self.logger = logger_initializer.init_log("as_engine", "as_engine.log")
        self.devices = {}

    def add_device(self, device):
        """ Add a new device into the dictionnary devices """
        # Verifying that the type of device is the good type.
        # Dictionnary's key is the device ID.
        if isinstance(device, SensorDevice):
            self.devices[device.get_device_id()] = device
        else:
            self.logger.warning("Class.Sensors :: add_data :: Error while adding the device object into devices. Device type : [%s] Waiting an object [SensorDevice]" %(type(device)))

    def add_data(self, data, device_id):
        """ Method that add a new RecordData into the recorded data list of the device """
        # Verifying the type of data.
        if isinstance(data, RecordData):
            self.devices[device_id].add_data(data)
        else:
            self.logger.warning("Class.Sensors :: add_data :: Error while adding the data object into data_list. Data type : [%s] Waiting an object [RecordData]" %(type(data)))

    def get_devices(self):
        """ Return the dictionnary of the devices as values and the IDs as keys """
        return self.devices

    def __str__(self):
        """ Return a string of all sensors """
        list_str = "List of all devices :\n\n"
        for device_id in self.devices.keys():
            list_str = list_str + self.devices[device_id].get_name_and_id()

        return list_str


class Engine:
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
        self.logger = logger_initializer.init_log("as_engine", "as_engine.log")
        self.__sensors_db = Sensors()
        self.__database_engine = database_manager.DatabaseEngine()
        self.new_device("Adeunis", "0018B20000000167")
        self.new_device("Watteco", "70B3D5E75E000239")

    def general_engine(self, xml_file):
        """Method that receive the xml file and calls every function to get data and save it into the database"""
        data_from_xml = self.parse_xml(xml_file)
        self.decode_and_add_record(data_from_xml[0], data_from_xml[1], data_from_xml[2])

    def save_data_file(self, xml_file):
        """ This method creates a xml file with the DATA from the POST method and save it into path DATA """

        # We take the date for named the new xml file.
        date = time.localtime()
        file_name = "./DATA/" + str(date.tm_mday) + "_" + str(date.tm_mon) + "_" + str(date.tm_year) + "_" + str(date.tm_hour) + "_" + str(date.tm_min) + "_" + str(date.tm_sec)

        with open(file_name, "w") as new_xml_file:
            new_xml_file.write(xml_file)

        new_xml_file.close()
        self.logger.info("Class.Engine :: save_data_file :: Save a new .xml file.")
        return file_name

    def parse_xml(self, file):
        """Method for parse the xml file"""

        date = datetime(2000, 1, 1, 0, 0, 0)
        device_id = ""
        payload = ""

        with open(file) as xml_file:
            xml = xml_file.read()

        xml_file.close()

        root = etree.fromstring(xml)

        for sub_element in root:
            if(sub_element.tag[30:] == "Time"):
                year = int(sub_element.text[:4])
                month = int(sub_element.text[5:7])
                day = int(sub_element.text[8:10])
                hour = int(sub_element.text[11:13])
                minute = int(sub_element.text[14:16])
                second = int(sub_element.text[17:19])
                date = datetime(year, month, day, hour, minute, second)
            elif(sub_element.tag[30:] == "DevEUI"):
                device_id = sub_element.text
            elif(sub_element.tag[30:] == "payload_hex"):
                payload = sub_element.text

        self.logger.info("Class.Engine ::parse_xml :: Parse .xml file.")
        return (device_id, date, payload)

    def watteco_decoder(self, data):
        """Method for decode the hex payload from a Watteco sensor"""
        length_data = len(data)

        if length_data != 114 :
            self.logger.warning("Class.Engine :: watteco_decoder :: Payload lenght isn't correct.")
        else :
            # Decoding the payload.
            version = int(data[0])
            payload_len = int(data[10:12], 16)
            nexthdr = data[12:14]
            hop_limit = int(data[14:16], 16)
            saddr = data[16:48]
            daddr = data[48:80]
            udp_port_source = int(data[80:84], 16)
            udp_port_dest = int(data[84:88], 16)
            length_udp = int(data[88:92], 16)
            checksum = data[92:96]
            raw_payload = data[96:114]
            mesured_value = (float(int(data[110:114], 16)))/100

            # We creating and return the mesured values list.
            new_data = RawData("Temperature", mesured_value)
            list_recorded_data=[new_data]

            return list_recorded_data

    def adeunis_decoder(self, data):
        """Method for decode the hex payload from an Adeunis LoRaWan Demonstrator sensor"""

        length_data = len(data)

        if ((length_data == 16) or (lenght_data == 12)): # Only temperature
            temp = float(int(data[2:4], 16))
            uplink_counter = int(data[4:6], 16)
            downlink_counter = int(data[6:8], 16)
            battery = float(int(data[8:12], 16))/1000
            latitude = 0
            longitude = 0

            new_data = RawData("Longitude", longitude)
            new_data_2 = RawData("Latitude", latitude)
            new_data_3 = RawData("Temperature", temp)

            list_recorded_data=[new_data, new_data_2, new_data_3]

            return list_recorded_data

        elif length_data == 28 : # Temperature + GPS
            temp = int(data[2:4], 16)
            latitude_degrees = data[4:6]
            latitude_minutes = data[6:11]
            hemisphere_latitude = data[11:12]
            longitude_degrees = data[12:15]
            longitude_minutes = data[15:19]
            hemisphere_longitude = data[19:20]
            uplink_counter = int(data[20:22], 16)
            downlink_counter = int(data[22:24], 16)
            battery= float(int(data[24:28], 16))/1000

            latitude = float(latitude_degrees + "." + str(int((int(latitude_minutes)/60)*10000000000)))
            if int(hemisphere_latitude) > 0:
                latitude *= -1

            longitude = float(longitude_degrees + "." + str(int((int(longitude_minutes)/60)*10000000000)))
            if int(hemisphere_longitude) > 0:
                longitude *= -1

            new_data = RawData("Longitude", longitude)
            new_data_2 = RawData("Latitude", latitude)
            new_data_3 = RawData("Temperature", temp)

            list_recorded_data=[new_data, new_data_2, new_data_3]

            return list_recorded_data

        else :
            self.logger.info("Class.Engine :: adeunis_decoder :: Payload lenght isn't correct")

    def new_device(self, name, device_id):
        """ This method creates and add a new sensor object to the database Sensors object """

        if (device_id in self.__sensors_db.get_devices()):
            self.logger.info("Class.Engine :: new_device :: Device [%s] %s already in the object device list"%(device_id, name))
        else:
            new_sensor = SensorDevice(name, device_id)
            self.__sensors_db.add_device(new_sensor)

        if not self.__database_engine.data_exist("Device", device_id):
            self.logger.info("Class.Engine :: new_device :: Device [%s] %s already in the sqlite database"%(device_id, name))
        else:
            self.__database_engine.insert("Device", ["Id", "Model"], [device_id, name])

    def decode_and_add_record(self, device_id, date, data):
        """This method decodes the payload, creates the objects related and add them into the databases"""
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        name_device = self.__sensors_db.get_devices()[device_id].get_model()

        name_decoder_function = name_device.lower() + "_decoder"
        decode = getattr(self, name_decoder_function)
        list_recorded_data = decode(data)

        raw_list = []
        i = 0
        while i < len(list_recorded_data):
            raw_list.append(list_recorded_data[i].get_value())
            i += 1


        new_record = RecordData(date, list_recorded_data)
        self.__sensors_db.get_devices()[device_id].add_data(new_record)

        self.__database_engine.get_columns("Watteco")

        if not self.__database_engine.record_exist(name_device, date): # Test if the record isn't exist by comparing the dates.
            self.logger.info("Class.Engine :: new_device :: Record from %s the %s already in the sqlite database."%(name_device, date))
        else :
            columns = self.__database_engine.get_columns(name_device)
            data_to_add = raw_list + [date, device_id]
            self.__database_engine.insert(name_device, columns, data_to_add)

    def get_sensors_db(self):
        """Return the object oriented database of sensor"""
        return self.__sensors_db

    def close_database_connection(self):
        """Method for close the connection with de sqlite3 database"""
        self.__database_engine.close_connection()

    def save_data_file(self, xml_file=""):
        """
            This method creates a xml file
            with the DATA from the POST method
            and save it into the path DATA
        """

        # We take the date of the execution for named the new xml file.
        date = time.localtime()
        file_name = "./DATA/" + str(date.tm_mday) + "_" + str(date.tm_mon) + "_" + str(date.tm_year) + "_" + str(date.tm_hour) + "_" + str(date.tm_min) + "_" + str(date.tm_sec)

        with open(file_name, "w") as new_xml_file:
            new_xml_file.write(xml_file)

        new_xml_file.close()
        return file_name


if __name__ == '__main__':
    engine = Engine()

    # Test parsing xml.
    engine.parse_xml("./xml.xml")

    ## Test adding device.
    engine.new_device("Adeunis", "0018B20000000167")
    engine.new_device("Adeunis", "0018B20000000167") # insert error check
    engine.new_device("Watteco", "70B3D5E75E000239")
    device_db_object = engine.get_sensors_db()

    ## Tests decode functions.
    engine.decode_and_add_record("0018B20000000167", datetime(2016, 1, 1, 0, 0, 0), "8e3036840b050000")
    engine.decode_and_add_record("0018B20000000167", datetime(2016, 1, 2, 0, 0, 1), "9e31485592200021746034830b1c")
    engine.decode_and_add_record("70B3D5E75E000239", datetime(2016, 1, 3, 0, 0, 2), "6000000000111140000000000000000070b3d5e75e0002390000000000000000000000ff00000000f0b5f0b400111b79110a0402000029091d")
    # Latitude : 48559220
    # Long : 00217460

    engine.general_engine("./xml.xml")

    engine.close_database_connection()
