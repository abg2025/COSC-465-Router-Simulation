from switchyard.lib.userlib import * # got this from the pdf

# the router class would take in the 'net' object (which is the Switchyard network
# object) and the 'interfaces' dictionary, where keys are the interface names and 
# values are tuples containing IP address, subnet mask, and MAC address for each interface
class Router:
    
    def __init__(self, net, interfaces):
        # constructor for router class, initializes the router with Switchyard network object and itnerfaces diciontary
        self.net = net # switchyard network object
        self.interfaces = interfaces # dictionary containing interface information (ip, subnet mask, mac address)
        self.routing_table = {} # initialize empty routing table

    # responsible for handling incoming pakcets, distinguishing ARP requests from
    # other types of packets, and calling the approporiate hangling method
    def process_packet(self, timestamp, input_port, packet):
        # get_header is a switchyard method used to retrieve the ehader of a 
        # specific protocol from a pakcet
        eth_packet = packet.get_header(Ethernet) # retrieves the ethernet header from packet
        if eth_packet is None:
            return
        
        if eth_packet.dst == self.interfaces[input_port][2]:
            # packet is destined for this router
            # checking if destination mac address matches router's interface mac address
            if isinstance(packet.get_header(Arp), Arp):
                # handle ARP request
                self._handle_arp_request(timestamp, input_port, packet)
            else:
                # handle other types of packets (e.g., IP)
                self._handle_ip_packet(timestamp, input_port, packet)

    # handles ARP requests and sends ARP replies if the target UP address mathces
    # any of the router's interfaces (?????)
    def _handle_arp_request(self, timestamp, input_port, packet):
        arp_header = packet.get_header(Arp)
        if arp_header is None or arp_header.operation != ArpOperation.Request:
            return
        
        target_ip = arp_header.targetprotoaddr # get target ip address from arp request
        for intf, (ip, mask, mac) in self.interfaces.items():
            # iterate over router's interfaces to find match for target ip address
            if ip == target_ip:
                # if target ip matches interface ip, send arp reply
                arp_reply = create_ip_arp_reply(mac, arp_header.senderhwaddr, ip, arp_header.senderprotoaddr)
                # create_ip_arp_reply is a swtichyard method used to create an arp reply packet
                # it takes the mac address of the replying interface, the mac address of the sender,
                # the ip address of the replying interface, and the ip address of the sender as arguments
                # and returna an arp reply packet
                self.net.send_packet(input_port, arp_reply)
        return

    # should be implemented to handle other types of IP packets, such as forwarding
    # packets based on the routing table
    def _handle_ip_packet(self, timestamp, input_port, packet):
        #TODO
        return

    # sends packets out through the specified output port
    def send_packet(self, output_port, packet):
        self.net.send_packet(output_port, packet)
        # send packet using switchyard's send_packet method
        # send_packet is invpoked on the net object, which is the swtichyard network object
        # this method sends the specific pakcet through the specific port in the network simulation
    
