from switchyard.lib.userlib import *
import router
import json
import packet
import simulation

# def create_interfaces(s):
#     obj = simulation.JSON("network_config_test")
#     config = obj.load_network_config()
#     for interface in config:
#         for details in interface:
#             s.add_interface(details['name'], details['mac_addr'], ipaddr=details['ip'])


# def tests():
#     s = TestScenario("Simulating Network")


#     # Setup: Add interfaces (nodes)
#     create_interfaces(s)

#     # Expected ARP request packet from router to discover Client1's MAC
#     router_broadcast_packet = packet.Packet("192.168.1.1", "00:00:00:00:01:01", "192.168.1.2", "00:00:00:00:02:01")
#     expected_arp_req = router_broadcast_packet.create_arp_request()

#     # Expectation: Router broadcasts ARP request to find Client1's MAC address
#     s.expect(PacketOutputEvent("Router1", expected_arp_req, display=Ethernet), "The router should broadcast an ARP request to discover Client1's MAC address.")

#     return s

#log_debug("Test")
scenario = TestScenario("test")