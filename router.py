from packet import Packet 
import ipaddress
class Router:
    def __init__(self, name, ip, mask, mac_addr, network):
        self.name = name
        self.ip = ip
        self.mask = mask
        self.mac_addr = mac_addr
        self.network = network
        self.routing_table = []
        self.arp_table = {}

    def receive_packet(self, packet):
        print("recieved")
        self.process_packet(packet)

    def process_packet(self, packet):
        if packet.packet_type == 'ARP':
            self.handle_arp_reply(packet)
        elif packet.packet_type == 'IP':
            self.handle_ip(packet)

    def handle_arp_reply(self, packet):
        if packet.dest_ip == self.ip:
            if packet.payload['operation'] == 'request':
                print("Router Recieved")
                # Respond to ARP request
                arp_reply = Packet(self.ip, self.mac_addr, packet.source_ip, packet.src_mac_addr, 'ARP',{'operation': 'reply'})
                self.network.send_packet(arp_reply)  # Send reply directly to the requester's MAC address
                # Update ARP table with requester's IP and MAC
                self.arp_table[packet.source_ip] = packet.src_mac_addr
            if packet.payload['operation'] == 'reply':
                # Update ARP table when a reply is received
                self.arp_table[packet.source_ip] = packet.src_mac_addr
                print("Added Client to {}".format(self.name))

    def is_ip_in_subnet(self, ip1, ip2):
        ip1 = ipaddress.ip_address(ip1)
        ip2 = ipaddress.ip_address(ip2)
        return ip1 in ip2

    def handle_ip(self, packet):
        destination = packet.dest_ip
        for route in self.routing_table:
            if self.is_ip_in_subnet(destination, self.ip + self.mask):
                if not self.arp_table[destination]:
                    self.perform_arp_request(self, destination)
            if destination == route['dest_ip']:
                next_hop_ip = route['next_hop_ip']
                next_hop_mac = self.network.resolve_mac(next_hop_ip)
                packet.dest_mac_addr = next_hop_mac
                packet.src_mac_addr = self.mac_addr
                self.network.send_packet(packet, next_hop_mac)
                return
        print("No route found for IP: {}".format(destination))

    def perform_arp_request(self, dest_ip):
        # Broadcast ARP request to resolve IP address to MAC address
        arp_request = Packet(self.ip, self.mac_addr, dest_ip, 'FF:FF:FF:FF:FF:FF', 'ARP', {'operation': 'request'})
        self.network.send_packet(arp_request)
        

