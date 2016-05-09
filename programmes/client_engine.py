#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

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

    def watteco_decoder(self, data):
        """Function that decode the hex data from a Watteco 3.1 sensor"""
        lenght_data = len(data)

        if lenght_data != 114 :
            return "Error, payload size is not correct."
        else :
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
            mesured_value = (float(int(data[110:114], 16)))/100 # PayLoad OK

            ## Créer l'objet correspondant.


    def adeunis_lorawan_demonstrator_decoder(self, data):
        """Function that decode the hex data from an Adeunis LoRaWan Demonstrator sensor"""

        lenght_data = len(data)

        if lenght_data == 12 : # Only temperature
            temp = int(data[2:4], 16)
            uplink_counter = int(data[4:6], 16)
            downlink_counter = int(data[6:8], 16)
            battery = float(int(data[8:12], 16))/1000

        elif lenght_data == 28 : # Temperature + GPS
            temp = int(data[2:4], 16)
            latitude = data[4:12]
            longitude = data[12:20]
            uplink_counter = int(data[20:22], 16)
            downlink_counter = int(data[22:24], 16)
            battery= float(int(data[24:28], 16))/1000

        else :
            return "Error, payload size is not correct."

    #def new_device(self, ):



class sensors:
    """
        This is a little database with the list of all sensor device and their recorded data.
    """

    def __init__(self):
        self.devices = {}

    def add_device(self, device):
        # On vérifie lorsqu'on ajoute un device au dictionnaire que c'est bien un objet de type "sensor_device"
        # La clé du dictionnaire est l'ID du device car unique et propre à chaque devices.
        if isinstance(device, sensor_device):
            self.devices[device.device_id] = device
        else:
            return "Error while adding the device object into devices.\n device type : %s\nWaiting an object [SENSOR_DEVICE]\n" %(type(device))

    def add_data(self, data, device_id):
        # On vérifie lorsqu'on ajoute l'objet data à la liste que c'est bien un objet de type "record_data"
        if isinstance(data, record_data):
            self.devices[device_id].add_data(data)
        else:
            return "Error while adding the data object into data_list.\n data type : %s\nWaiting an object [RECORD_DATA]\n" %(type(data))


class sensor_device:
    """
        It's an object that contains information about a particular sensor :
            - Device's ID.
            - Device's name (Watteco or Adeunis for example).
            - all recorded data from a sensor_device.
    """

    def __init__(self, name, device_id):
        self.name = name
        self.device_id = device_id
        self.data_list = []

    def add_data(self, data):
        # On vérifie lorsqu'on ajoute l'objet data à la liste que c'est bien un objet de type "record_data"
        if isinstance(data, record_data):
            self.data_list.append(data)
        else:
            return "Error while adding the data object into data_list.\n data type : %s\nWaiting an object [RECORD_DATA]\n" %(type(data))


    def number_of_registered_data(self):
        return "Number of registered data : %s" %(len(self.data_list))

    def list_all_data(self):
        for i in data_list :
            return data_list[i]


class record_data:
    """
        It's an object that represents a record from a sensor.
        It is specified by the date of the record and a list of the data recorded by the sensor.
    """

    def __init__(self, date, data_list):
        self.date = date
        # On vérifie que data_list est bien une liste.
        if isinstance(data_list, list):
                self.data_list = data_list
        else:
            return "Error while creating the record_data object.\n data_list type : %s\nWaiting an object [LIST]\n" %(type(data_list))


    def __str__(self):
        string = "Date : %s\nData :\n" %(self.date)
        for i in data_list :
            string = string + self.data_list[i]

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

    def __str__(self):
        return "Type : %s\tValue : %s\n" %(self.data_type, self.value)


        print(version, payload_len, nexthdr, hop_limit, saddr, daddr, udp_port_source, udp_port_dest, lenght_udp, checksum, raw_payload, mesured_value)



engine = engine()
engine.watteco_decoder("6000000000111140000000000000000070b3d5e75e0002390000000000000000000000ff00000000f0b5f0b400111b79110a0402000029091d")
engine.adeunis_lorawan_demonstrator_decoder("8e3036840b05")
engine.adeunis_lorawan_demonstrator_decoder("9e31485592200021746034830b1c")
