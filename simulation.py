#!/usr/bin/env python3

from switchyard.lib.userlib import *
# import router
# import json
# import client 

# class JSON:
#     def __init__(self, file_path):
#         self.file_path = file_path
    
#     def load_network_config(self):
#         with open(self.file_path, 'r') as file:
#             config = json.load(file)
#         return config
    
# class Simulation:
#     def __init__(self, net, config) -> None:
#         self.routers = {}
#         self.clients = {}
#         self.net = net
#         self.config = config 
#         pass

#     def setup_network(self):
#         # Initialize routers based on the JSON config
#         for router_info in self.config.get('routers'):

#             self.routers[router_info['name']] = router.Router(self.net, router_info['name'], router_info['ip'], router_info['mask'], router_info['mac_addr'])

#         # Example of initializing client behavior
#         for client_info in self.config.get('clients'):
#             self.clients[client_info['name']] = client.Client(self.net, client_info['ip'], client_info['mac'], client_info['name'])
#             # client logic 

#     @property
#     def getRouters(self):
#         return self.routers 
    
#     @property
#     def getClients(self):
#         return self.clients
    
def main(net):
    # Load and parse the JSON configuration
    # json_file = JSON("network_config_test.json")
    # config = json_file.load_network_config()
        
    # # Setup the network based on the JSON configuration
    # simulation = Simulation(net, config)
    # simulation.setup_network()

    # nodes = net.interfaces()

    # while True:
    #     try:
    #         timestamp,dev,packet = net.recv_packet()
    #     except NoPackets:
    #         continue
    #     except Shutdown:
    #         return
    #     log_debug ("In {} received packet {} on {}".format(net.name, packet, dev))
    #     eth = packet.get_header(Ethernet)
    #     if eth is None:
    #         log_info("Received a non-Ethernet packet?!")
    #         continue
    
    #     net.shutdown()
    pass

