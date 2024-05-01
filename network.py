import json
import ipaddress
from router import Router
from client import Client

class Network:
    def __init__(self, config_file):
        # initialize empty dictionaries to store devices and connections 
        self.devices = {}
        self.connections = {}
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            # set up network based on the loaded configuration
            self.setup_network(config)

    def setup_network(self, config):
        # Create devices

        # routers
        for router_info in config['routers']:
            # create router instance
            router = Router(router_info['name'], router_info['ip'], router_info['mask'], router_info['mac_addr'], self)
            # initialize OSPF routing protocol for the router
            router.initialize_ospf()
            # add router to devices dictionary
            self.devices[router_info['name']] = router

        # clients
        for client_info in config['clients']:
            # create client instance and add client to devices dictionary
            self.devices[client_info['name']] = Client(client_info['name'], client_info['ip'], client_info['gateway'], client_info['mac_addr'], self)

    def get_router_by_ip(self, ip):
        # find a router with the specified ip address
        for device_name, device in self.devices.items():
            if isinstance(device, Router) and device.ip == ip:
                return device
        return None
    
    def is_ip_in_subnet(self, ip1, ip2):
        # check if ip1 is in the same subnet as IP2
        ip1 = ipaddress.IPv4Address(ip1)
        ip2 = ipaddress.IPv4Address(ip2)
        network_address = ipaddress.IPv4Network(ip2.exploded + "/24", strict=False)
        return ip1 in network_address
                
    def send_broadcast_packet(self, packet):
        # send a broadcast packet to all devices in the same subnet as the source ip
        for device_name, device in self.devices.items():
            if self.is_ip_in_subnet(device.ip, packet.source_ip) and device.ip != packet.source_ip:
                device.receive_packet(packet)

    def send_ospf_packet(self, packet):
        # send an OSPF packet to the destination router
        dest_router = self.get_router_by_ip(packet.dest_ip)
        if dest_router != None:
            dest_router.recieve_packet(packet)
        else:
            print("No router found for OSPF packet destination IP: {}".format(packet.dest_ip))

    def send_normal_packet(self, packet):
        # send a normal packet to the destination device
        for device_name, device in self.devices.items():
            if packet.dest_ip == device.ip:
                device.receive_packet(packet)
                return 

    def send_packet(self, packet):
        # determine packet type and route accordingly
        if packet.packet_type == 'OSPF':
            self.send_ospf_packet(packet)
        elif packet.dest_mac_addr == 'FF:FF:FF:FF:FF:FF':
            self.send_broadcast_packet(packet)
        else:
            self.send_normal_packet(packet)

