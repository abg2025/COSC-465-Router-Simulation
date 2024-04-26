class Packet:
    def __init__(self, source_ip, src_mac_addr, dest_ip, dest_mac_addr, packet_type, payload='', ttl=64, size=0, seq_num=None, ack_num=None, flags=None):
        self.source_ip = source_ip
        self.src_mac_addr = src_mac_addr
        self.dest_ip = dest_ip
        self.dest_mac_addr = dest_mac_addr
        self.packet_type = packet_type
        self.payload = payload
        self.ttl = ttl
        self.size = size if size else self.estimate_size()
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.flags = flags
        self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        checksum = sum(ord(c) for c in str(self.payload)) % 256
        checksum += sum(ord(c) for c in self.source_ip + self.dest_ip + self.src_mac_addr + self.dest_mac_addr) % 256
        return checksum

    def verify_checksum(self):
        return self.calculate_checksum() == self.checksum

    def estimate_size(self):
        base_size = 20  # Basic IP header size
        if self.packet_type == 'TCP':
            base_size += 20  # Add TCP header size
        elif self.packet_type == 'ARP':
            base_size += 28  # Add ARP header size
        return base_size + len(self.payload)

    def __str__(self):
        return "Packet({}): {} -> {}, Size: {} bytes".format(self.packet_type, self.source_ip, self.dest_ip, self.size)
