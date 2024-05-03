import unittest
from packet import Packet
from network import Network

class TestNetworkSimulation(unittest.TestCase):
    def setUp(self):
        """Setup the network from a JSON file."""
        self.network = Network("network_config_1router.json")

    def test_packet_transfer(self): #Test case can be used for all three created json files 
        """Test if a packet sent from ClientA reaches ClientB."""
        clientA = self.network.devices['ClientA']
        clientB = self.network.devices['ClientB']
        packet = Packet(clientA.ip, clientA.mac_addr, clientB.ip, clientB.mac_addr, "IP", "Hello, ClientB!")
        clientA.send_packet(packet)
        self.assertTrue(packet in clientB.received_packets)
    
    def test_packet_transfer2(self): #Test case can be used for network_config_dynamic.json comment out if using another json file
        """Test if packet sent from ClientA reaches ClientC"""
        clientA = self.network.devices['ClientA']
        clientC = self.network.devices['ClientC']
        packet = Packet(clientA.ip, clientA.mac_addr, clientC.ip, clientC.mac_addr, "IP", "Hello, ClientC!")
        clientA.send_packet(packet)
        self.assertTrue(packet in clientC.received_packets)
    

if __name__ == '__main__':
    unittest.main()
