class Packet:
    def __init__(self, source_ip, src_mac_addr, dest_ip, dest_mac_addr, packet_type, payload=''):
        self.source_ip = source_ip
        self.src_mac_addr = src_mac_addr
        self.dest_ip = dest_ip
        self.dest_mac_addr = dest_mac_addr
        self.packet_type = packet_type
        self.payload = payload
        self.checksum = self.calculate_checksum()
        print(self)

    def calculate_checksum(self):
        checksum = sum(ord(c) for c in str(self.payload)) % 256
        checksum += sum(ord(c) for c in self.source_ip + self.dest_ip + self.src_mac_addr + self.dest_mac_addr) % 256
        return checksum

    def verify_checksum(self):
        return self.calculate_checksum() == self.checksum

    def __str__(self):
        return "Packet({}): {} -> {}".format(self.packet_type, self.source_ip, self.dest_ip)
