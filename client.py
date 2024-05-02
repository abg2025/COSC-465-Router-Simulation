from packet import Packet
import time 
class Client:
    def __init__(self, name, ip, gateway, mac_addr, network):
        self.name = name
        self.ip = ip
        self.gateway = gateway
        self.mac_addr = mac_addr
        self.network = network
        self.received_packets = []  # List to store received packets
        self.arp_table = {}  # Initialize ARP table for IP-to-MAC resolutions

    def send_packet(self, packet):
        # Lookup destination MAC address in the ARP table, use broadcast address if not found
        dest_mac = self.arp_table.get(self.gateway, 'FF:FF:FF:FF:FF:FF')
        if dest_mac == 'FF:FF:FF:FF:FF:FF':
            # Send ARP request and wait for ARP reply
            self.send_arp_packet()
            # Wait for a short period to receive ARP reply
            time.sleep(1)
            dest_mac = self.arp_table.get(self.gateway, 'FF:FF:FF:FF:FF:FF')  # Try again after waiting

        # If ARP reply was received or found in ARP table, send the packet
        if dest_mac != 'FF:FF:FF:FF:FF:FF':
            self.network.send_packet(packet, self.ip, self.gateway)
        else:
            print("Unable to find Router MAC Address with IP Address {}")
        

    def send_arp_packet(self):
        packet_type = "ARP"
        data = {"operation": "request"}
        packet = Packet(self.ip, self.mac_addr, self.gateway, 'FF:FF:FF:FF:FF:FF', packet_type, payload=data)
        self.network.send_packet(packet, self.ip, self.gateway)  # Send using device name as identifier

    def receive_packet(self, packet):
        if packet.verify_checksum():
            self.received_packets.append(packet)  # Store the packet if checksum is valid
            print("Received valid packet at {}: {}".format(self.ip, packet.payload))
            if packet.packet_type == 'ARP' and packet.payload['operation'] == 'reply':
                # Update ARP table if ARP reply received
                self.arp_table[packet.source_ip] = packet.src_mac_addr
            elif packet.packet_type == 'ARP' and packet.payload['operation'] == 'request':
                self.handle_arp_packet(packet)
        else:
            print("Packet checksum invalid, discarding packet.")

    def perform_arp_request(self, dest_ip):
        # Broadcast ARP request to resolve IP address to MAC address
        arp_request = Packet(self.ip, self.mac_addr, dest_ip, 'FF:FF:FF:FF:FF:FF', 'ARP', {'operation': 'request'})
        self.network.send_packet(arp_request)

    def handle_arp_packet(self, packet):
        # Respond with ARP reply
        arp_reply = Packet(self.ip, self.mac_addr, packet.source_ip, packet.src_mac_addr, 'ARP', {'operation': 'reply'})
        self.network.send_packet(arp_reply, self.ip, packet.source_ip)

