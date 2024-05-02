import heapq
from packet import Packet 
import ipaddress
import time

class Router:
    def __init__(self, name, ip, mask, mac_addr, network):
        # initialize router attributes
        self.name = name # router name
        self.ip = ip # router ip address
        self.mask = mask # subnet mask
        self.mac_addr = mac_addr # mac address
        self.network = network # reference to the network
        self.routing_table = [] # routing table
        self.arp_table = {} #arp table
        self.ospf_neighbors = set()  # OSPF neighbors
        self.lsdb = {}  # Link State Database

    def receive_packet(self, packet):
        # handle incoming packets based on their types
        if packet.packet_type == 'ARP':
            self.handle_arp_reply(packet)
        elif packet.packet_type == 'IP':
            self.handle_ip(packet)
        elif packet.packet_type == 'OSPF':
            self.handle_ospf_packet(packet)

    def handle_arp_reply(self, packet):
        # handle arp reply packets
        if packet.payload['operation'] == 'request':
            # send arp reply back
            arp_reply = Packet(self.ip, self.mac_addr, packet.source_ip, packet.src_mac_addr, 'ARP', {'operation': 'reply'})
            self.network.send_packet(arp_reply)
            # update arp table with the sender's ip and mac addresses
            self.arp_table[packet.source_ip] = packet.src_mac_addr
        elif packet.payload['operation'] == 'reply':
            # update arp table with the sender's ip and mac addresses
            self.arp_table[packet.source_ip] = packet.src_mac_addr
        
    def is_ip_in_subnet(self, ip1, ip2):
        # check if ip1 is in the same subnet as IP2
        ip1 = ipaddress.IPv4Address(ip1)
        ip2 = ipaddress.IPv4Address(ip2)
        network_address = ipaddress.IPv4Network(ip2.exploded + "/24", strict=False)
        return ip1 in network_address

    def handle_ip(self, packet):
        # handle ip packets
        destination = packet.dest_ip
        # check if destination mac address is known
        if not self.arp_table[destination]:
            # if destination is in the same subnet, perform arp request
            if self.is_ip_in_subnet(destination, self.ip + self.mask):
                self.perform_arp_request(self, destination)
                # check if destination ip is in the routing table
                time.sleep(1)
        for route in self.routing_table:
            if destination == route['dest_ip']:
                next_hop_ip = route['next_hop_ip']
                next_hop_mac = self.network.resolve_mac(next_hop_ip)
                # update packet with next hop mac address
                packet.dest_mac_addr = next_hop_mac
                packet.src_mac_addr = self.mac_addr
                # send packet to the next hop
                self.network.send_packet(packet, )
                return
        print("No route found for IP: {}".format(destination))
    
    def perform_arp_request(self, dest_ip):
        # perform arp request for the destination ip
        arp_request = Packet(self.ip, self.mac_addr, dest_ip, 'FF:FF:FF:FF:FF:FF', 'ARP', {'operation': 'request'})
        self.network.send_packet(arp_request)
    

    #given the network address, cost, next_hop add into routing table where the key is the network_address 
    def update_routing_table(self, network_address, cost, next_hop):
        pass
        

   

    #This function will create the RIP packets that will be sent to its neighbors via the network class. To get the routers neighbors just use self.network.get_neighbors(self.ip)
    def initialize_distance_vector(self):
        pass
        
        

           
