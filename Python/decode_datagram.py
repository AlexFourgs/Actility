#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

# This program decode a datagram from the internet. It only work with TCP.
# Object that represent the ethernet adress
class EthernetAdress:

    addr_ethernet="00:00:00:00:00:00"
    source = False
    dest = False

    # Initialisation function / Constructor
    def __init__(self, addr_ethernet="00:00:00:00:00:00", source=False, dest=False):
        self.addr_ethernet = addr_ethernet
        self.source = source
        self.dest = dest

    def __str__(self):
        if self.source == True:
            return "The source ethernet adress is : %s" %(self.addr_ethernet)
        elif self.dest == True:
            return "The destination ethernet adress is : %s" %(self.addr_ethernet)
        else:
            return "Error, we don't if it's the source or the destination adress"

    def __eq__(self, other):
        return self.addr_ethernet == other

    def __ne__(self, other):
        return self.addr_ethernet != other


class DatagramEthernet:

    source = EthernetAdress()
    dest = EthernetAdress()
    type_ip = ""

    def __init__(self, source = EthernetAdress(), dest = EthernetAdress(), type_ip = ""):
        self.source = source
        self.dest = dest
        self.type_ip = type_ip

    def __str__(self):
        return str("%s\n%s\nThe type is %s\n" % (self.dest, self.source, self.type_ip))


def decode_ethernet(datagram = ""):
    """ Function that parse the ethernet datagram. """
    longueur_datagram = len(datagram)
    dest = ""
    source = ""
    type_ip = ""

    if longueur_datagram != 41:
        print("[DECODE ETHERNET] Error : the datagram is too short or too long")
    else:
        i = 0
        byte = datagram.split(' ')

        # Destination
        while i < 6:
            if i != 5:
                dest = dest + byte[i]
                dest = dest + ":"
            else:
                dest = dest + byte[i]
                #dest = dest + datagram(i)

            i+=1

        eth_dest = EthernetAdress(dest, False, True)

        # Source
        while i < 12:
            if i != 11:
                source = source + byte[i]
                source = source + ":"
            else:
                source = source + byte[i]
            i+=1

        eth_source = EthernetAdress(source, True, False)


        # Type ip
        while i < 14:
            if i != 13:
                type_ip = type_ip + byte[i]
                type_ip = type_ip + " "
            else:
                type_ip = type_ip + byte[i]
            i+=1

        #print("Type ip = %s" % (type_ip))
        parsedEthdatagram = DatagramEthernet(eth_source, eth_dest, type_ip)

        return parsedEthdatagram

# Object that represent the ip adress
class IpAdress:

    addr_ip = "000.000.000.000"
    source = False
    dest = False

    # Initialisation function / Constructor
    def __init__(self, addr_ip = "000.000.000.000", source = False, dest = False):
        self.addr_ip = addr_ip
        self.source = source
        self.dest = dest

    def __str__(self):
        if self.source == True:
            return ("The source ip adress is : %s" %(self.addr_ip))
        elif self.dest == True:
            return ("The destination ethernet adress is : %s" %(self.addr_ip))
        else:
            return "Error, we don't if it's the source or the destination adress"

    def __eq__(self, other):
        return self.addr_ip == other

    def __ne__(self, other):
        return self.addr_ip != other

class DatagramIp:
    source = IpAdress()
    dest = IpAdress()
    protocol = ""

    def __init__ (self, source = IpAdress(), dest = IpAdress(), protocol = ""):
        self.source = source
        self.dest = dest
        self.protocol = protocol

    def __str__ (self):
        return("%s\n%s\nThe protocol is : %s\n" % (self.source, self.dest, self.protocol))


def decode_ip(datagram=""):
    """ This function decode the ip datagram. """
    datagram_length = len(datagram)
    protocol=""
    ip_src = ""
    ip_dest = ""

    if datagram_length != 59:
        print("Error lenght ip datagram.")
    else:
        bytes_hexa_tab = datagram.split(" ")

        protocol = str(int(bytes_hexa_tab[9], 16))

        i = 12
        while i < 16:
            if i != 15:
                ip_src = ip_src + str(int(bytes_hexa_tab[i], 16))
                ip_src = ip_src + "."
            else:
                ip_src = ip_src + str(int(bytes_hexa_tab[i], 16))
            i += 1

        add_ip_src = IpAdress(ip_src, True, False)

        while i < 20:
            if i != 19:
                ip_dest = ip_dest + str(int(bytes_hexa_tab[i], 16))
                ip_dest = ip_dest + "."
            else:
                ip_dest = ip_dest + str(int(bytes_hexa_tab[i], 16))
            i += 1

        add_ip_dest = IpAdress(ip_dest, False, True)

        parsed_datagram_ip = DatagramIp(add_ip_src, add_ip_dest, protocol)

        return parsed_datagram_ip


class PayLoad:
    data=""

    def __init__(self, data=""):
        self.data = data

    def __str__(self):
        return self.data


class DatagramProtocol:
    source_port = ""
    dest_port = ""
    checksum = ""
    protocol = ""
    payload = PayLoad()

    def __init__(self, source_port = "", dest_port = "", checksum = "", protocol = "", payload = PayLoad()):
        self.source_port = source_port
        self.dest_port = dest_port
        self.checksum = checksum
        self.protocol = protocol
        self.payload = payload

    def __str__(self):
        if self.protocol == 17:
            return ("[UDP PROTOCOL]\n Source port : %s\n Destination port : %s\n Checksum : %s\n Payload : %s\n" %(self.source_port, self.dest_port, self.checksum, self.payload))
        elif self.protocol == 6:
            return ("[TCP PROTOCOL]\n Source port : %s\nDestination port : %s\n Payload : %s\n" %(self.source_port, self.dest_port, self.payload))
        else:
            return "Unknown protocol"


def decode_protocol(datagram="", protocol=""):
    """ This function decode a protocol datagram"""

    if protocol == 17: # UDP
        return decode_udp(datagram)
    elif protocol == 6: # TCP
        return decode_tcp(datagram)
    else:
        print("Don't know this protocol")


def decode_udp (datagram=""):
    """ This function decode an UDP datagram"""
    source_port = ""
    dest_port = ""
    checksum = ""
    payload_data = ""
    payload = PayLoad()

    bytes_hexa_tab= datagram.split(" ")

    i = 0
    while i < 2:
        source_port = source_port + bytes_hexa_tab[i]
        i += 1

    source_port = str(int(source_port, 16))

    while i < 4:
        dest_port = dest_port + bytes_hexa_tab[i]
        i+= 1

    dest_port = str(int(dest_port, 16))

    i = 6 # For checksum

    while i < 8:
        checksum = checksum + bytes_hexa_tab[i]
        i+=1

    checksum = str(int(checksum, 16))


    while i < len(bytes_hexa_tab):
        payload_data = payload_data + bytes_hexa_tab[i]
        i+=1

    payload = PayLoad(payload_data)

    return DatagramProtocol(source_port, dest_port, checksum, 17, payload)

def decode_tcp(datagram=""):
    """ This function decode a TCP datagram """
    source_port = ""
    dest_port = ""
    checksum = ""
    payload = Payload()

    bytes_hexa_tab = datagram.split(" ")

    i = 0
    while i < 2:
        source_port = source_port + bytes_hexa_tab[i]
        i += 1

    source_port = str(int(source_port, 16))

    while i < 4:
        dest_port = dest_port + bytes_hexa_tab[i]
        i+= 1

    dest_port = str(int(dest_port, 16))

    i = 16 # For checksum

    while i < 18:
        checksum = checksum + bytes_hexa_tab[i]
        i+=1

    checksum = str(int(checksum, 16))

    i = 24 # For payload

    while i <= len(datagram):
        payload_data = payload_data + bytes_hexa_tab[i]
        i+=1

    payload = Payload(payload_data)

    return DatagramProtocol(source_port, dest_port, checksum, 6, payload)

class Datagram:
    datagram_ethernet = DatagramEthernet()
    datagram_ip = DatagramIp()
    datagram_protocol = DatagramProtocol()

    def __init__ (self, datagram_ethernet = DatagramEthernet(), datagram_ip = DatagramIp(), datagram_protocol = DatagramProtocol()):
        self.datagram_ethernet = datagram_ethernet
        self.datagram_ip = datagram_ip
        self.datagram_protocol = datagram_protocol

    def __str__ (self):
        return ("[ETHERNET INFORMATIONS]\n%s\n\n[IP INFORMATIONS]\n%s\n\n[PROTOCOL INFORMATIONS]\n%s\n\n" %(self.datagram_ethernet, self.datagram_ip, self.datagram_protocol))


def decode_datagram(datagram=""):
    datagram_eth_str = ""
    datagram_ip_str = ""
    datagram_prot_str = ""

    i = 0

    while i <= 40:
        datagram_eth_str = datagram_eth_str + datagram[i]
        i+=1

    i+=1
    while i <= 100:
        datagram_ip_str = datagram_ip_str + datagram[i]
        i+=1

    i+=1
    while i < len(datagram):
        datagram_prot_str = datagram_prot_str + datagram[i]
        i+=1


    datagram_eth = decode_ethernet(datagram_eth_str)
    datagram_ip = decode_ip(datagram_ip_str)
    datagram_prot = decode_protocol(datagram_prot_str, int(datagram_ip.protocol))

    return Datagram(datagram_eth, datagram_ip, datagram_prot)



### TESTS ###
datagram_str = raw_input("Enter the datagram :")
parsed_datagram = decode_datagram(datagram_str)
print(parsed_datagram)

# fe aa 16 98 17 ba 53 10 91 5e ac 82 08 00 45 00 7b 20 00 35 26 ac 40 11 aa b2 08 4e 4d 4b 45 e7 34 11 7b 20 00 43 09 18 00 6e aa b2 76 54 00 1b
