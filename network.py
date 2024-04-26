import json
import ipaddress
from router import Router
from client import Client

class Network:
    def __init__(self, config_file):
        self.devices = {}
        self.connections = {}
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            self.setup_network(config)

    def setup_network(self, config):
        # Create devices
        for router_info in config['routers']:
            self.devices[router_info['name']] = Router(router_info['name'], router_info['ip'], router_info['mask'], router_info['mac_addr'], self)
            print("Created")
        
        for client_info in config['clients']:
            self.devices[client_info['name']] = Client(client_info['name'], client_info['ip'], client_info['mask'], client_info['mac_addr'], self)
        print(len(self.devices))
    
    def is_ip_in_subnet(self, ip1, ip2):
        ip1 = ipaddress.IPv4Address(ip1)
        ip2 = ipaddress.IPv4Address(ip2)
        network_address = ipaddress.IPv4Network(ip2.exploded + "/24", strict=False)
        return ip1 in network_address
                

    def send_packet(self, packet):
        if packet.dest_mac_addr == 'FF:FF:FF:FF:FF:FF':
            # Handle broadcast
            try:
                for device_name, device in self.devices.items():
                    print("test")
                    if self.is_ip_in_subnet(device.ip, packet.source_ip) and device.ip != packet.source_ip:
                        print("Hi")
                        self.devices[device_name].receive_packet(packet)
            except Exception as e:
                print("No connections found for device: {} {}".format(packet.source_ip, e))
        else:
            # Normal packet sending
            for device_name, device in self.devices.items():
                if packet.dest_ip == device.ip:
                    self.devices[device_name].receive_packet(packet)
