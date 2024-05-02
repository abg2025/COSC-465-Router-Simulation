import json
import ipaddress
from router import Router
from client import Client
import threading

class Network:
    def __init__(self, config_file):
        # initialize empty dictionaries to store devices and connections 
        self.devices = {}
        self.connections = {}
        self.setup_semaphore = threading.Semaphore(1)
        self.is_network_setup = False
        self.load_config(config_file)
        

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            # set up network based on the loaded configuration
            self.setup_network(config)

    def get_device_by_ip(self, ip):
        # find a router with the specified ip address
        for device_name, device in self.devices.items():
            if  device.ip == ip:
                return device
        return None

    def setup_network(self, config):
        # Create devices
        self.setup_semaphore.acquire()
        try:
            if not self.is_network_setup:
                 # routers
                for router_info in config['routers']:
                    # create router instance
                    router = Router(router_info['name'], router_info['ip'], router_info['mask'], router_info['mac_addr'], self)
                    # initialize OSPF routing protocol for the router
                    # add router to devices dictionary
                    self.devices[router_info['name']] = router
                
                #setup direct links for routers
                for link in config['links']:
                    from_router = self.get_device_by_ip(link['from'])
                    to_router = self.get_device_by_ip(link['to'])
                    from_router.add_link(to_router)
                    to_router.add_link(from_router)
                    
                #Initialize RIP AKA Distance Vector Routing 
                for device_name, device in self.devices.items():
                    device.initialize_distance_vector()

                # clients
                for client_info in config['clients']:
                    # create client instance and add client to devices dictionary
                    self.devices[client_info['name']] = Client(client_info['name'], client_info['ip'], client_info['gateway'], client_info['mac_addr'], self)
        finally:
            self.setup_semaphore.release()

    
    def is_ip_in_subnet(self, ip1, ip2):
        # check if ip1 is in the same subnet as IP2
        ip1 = ipaddress.IPv4Address(ip1)
        ip2 = ipaddress.IPv4Address(ip2)
        network_address = ipaddress.IPv4Network(ip2.exploded + "/24", strict=False)
        return ip1 in network_address
                
    def send_broadcast_packet(self, packet, source_ip, dest_ip):
        # send a broadcast packet to all devices in the same subnet as the source ip
        for device_name, device in self.devices.items():
            if self.is_ip_in_subnet(device.ip, packet.source_ip) and device.ip != packet.source_ip:
                device.receive_packet(packet)

    def send_RIP_packet(self, packet, source_ip, dest_ip):
        # send an OSPF packet to the destination router
        dest_router = self.get_device_by_ip(packet.dest_ip)
        if dest_router != None:
            dest_router.receive_packet(packet)
        else:
            print("No router found for RIP packet destination IP: {}".format(dest_ip))

    def send_normal_packet(self, packet, source_ip, dest_ip):
        # send a normal packet to the destination device
        for device_name, device in self.devices.items():
            if dest_ip == device.ip:
                device.receive_packet(packet)
                return 

    def send_packet(self, packet, source_ip, dest_ip):
        # determine packet type and route accordingly
        print("Sending {} packet to {} from {}".format(packet.packet_type, source_ip,dest_ip))
        if packet.packet_type == 'RIP':
            self.send_RIP_packet(packet, source_ip, dest_ip)
        elif packet.dest_mac_addr == 'FF:FF:FF:FF:FF:FF':
            self.send_broadcast_packet(packet, source_ip, dest_ip)
        else:
            self.send_normal_packet(packet, source_ip, dest_ip)
        return

