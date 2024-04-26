from packet import Packet
class Client:
    def __init__(self, name, ip, mask, mac_addr, network):
        self.name = name
        self.ip = ip
        self.mask = mask
        self.mac_addr = mac_addr
        self.network = network
        self.received_packets = []  # List to store received packets
        self.arp_table = {}  # Initialize ARP table for IP-to-MAC resolutions

    def send_packet(self, packet, data):
        # Lookup destination MAC address in the ARP table, use broadcast address if not found
        dest_mac = self.arp_table.get(packet.dest_ip, 'FF:FF:FF:FF:FF:FF')
        if dest_mac == 'FF:FF:FF:FF:FF:FF':
            packet_type = "ARP"
            payload = {"operation": "request"}
        packet = Packet(self.ip, self.mac_addr, packet.dest_ip, dest_mac, packet_type, payload=data)
        self.network.send_packet(packet)  # Send using device name as identifier

    def receive_packet(self, packet):
        if packet.verify_checksum():
            self.received_packets.append(packet)  # Store the packet if checksum is valid
            print("Received valid packet at {}: {}".format(self.ip, packet.payload))
            if packet.packet_type == 'ARP' and packet.payload['operation'] == 'reply':
                # Update ARP table if ARP reply received
                self.arp_table[packet.source_ip] = packet.src_mac_addr
        else:
            print("Packet checksum invalid, discarding packet.")

    def perform_arp_request(self, dest_ip):
        # Broadcast ARP request to resolve IP address to MAC address
        arp_request = Packet(self.ip, self.mac_addr, dest_ip, 'FF:FF:FF:FF:FF:FF', 'ARP', {'operation': 'request'})
        self.network.send_packet(arp_request)

    def handle_arp_packet(self, packet):
        if packet.payload['operation'] == 'request' and packet.dest_ip == self.ip:
            # Respond with ARP reply
            arp_reply = Packet(self.ip, self.mac_addr, packet.source_ip, packet.src_mac_addr, 'ARP', {'operation': 'reply', 'target_mac': self.mac_addr, 'sender_mac': packet.src_mac_addr})
            self.network.send_packet(arp_reply, self.name)

