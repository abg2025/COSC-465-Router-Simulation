import unittest
from packet import Packet
from network import Network

class TestNetworkSimulation(unittest.TestCase):
    def setUp(self):
        """Setup the network from a JSON file."""
        self.network = Network("network_config_test.json")

    def test_packet_transfer(self):
        """Test if a packet sent from ClientA reaches ClientB."""
        clientA = self.network.devices['ClientA']
        clientB = self.network.devices['ClientB']
        router1 = self.network.devices
        packet = Packet("192.168.1.2", "00:00:00:00:02:01", "111.122.1.2", "00:00:00:00:02:02", "IP", "Hello, ClientB!")
        clientA.send_packet(packet, "Hi ClientB")
        self.assertTrue(("192.168.1.1" in clientA.arp_table.keys()) == True)

if __name__ == '__main__':
    unittest.main()
