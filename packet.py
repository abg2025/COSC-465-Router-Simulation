class Packet:
    num = 0
    def __init__(self, source_ip, src_mac_addr, dest_ip, dest_mac_addr, packet_type, payload=''):
        # initialize packet attributes
        self.source_ip = source_ip # source ip address
        self.src_mac_addr = src_mac_addr # source mac address
        self.dest_ip = dest_ip # destination ip address
        self.dest_mac_addr = dest_mac_addr # destination mac address
        self.packet_type = packet_type # type of packet 
        self.payload = payload # packet payload
        Packet.num += 1
        self.checksum = self.calculate_checksum() # calculate and set checksum
        print(self)

    def calculate_checksum(self):
        checksum = sum(ord(c) for c in str(self.payload)) % 256 # calculate checksum for payload
        # add checksum for ip addresses and mac addresses
        checksum += sum(ord(c) for c in self.source_ip + self.dest_ip + self.src_mac_addr + self.dest_mac_addr) % 256
        return checksum

    def verify_checksum(self):
        # compare calculated checksum with stored checksum
        return self.calculate_checksum() == self.checksum

    def __str__(self):
        # string representation of the packet
        return "Packet({}) No. {}: {} -> {}".format(self.packet_type, Packet.num, self.source_ip, self.dest_ip)
