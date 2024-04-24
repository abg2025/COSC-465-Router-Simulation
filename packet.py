from switchyard.lib.userlib import *

class Packet:
# should have source IP, source Mac address, destination IP, destination IP MAC address,
    


    def __init__(self,sourceIp,src_mac_addr,destIP,dest_mac_addr, packet_type):
        self.sourceIP = sourceIp
        self.src_mac_addr = src_mac_addr
        self.destIP = destIP
        self.dest_mac_addr = dest_mac_addr
        self.Packet = Packet()
        self.packet_type = packet_type
        

    def getSourceIP(self):
        return self.sourceIP
    
    def getMacAddr(self):
        return self.src_mac_addr
    
    def getDestIP(self):
        return self.destIP 
    
    def getDestMacAddr(self):
        return self.dest_mac_addr
    
    def create_arp_request(self):
        # Construct an ARP request packet
        ether = Ethernet()
        ether.src = self.src_mac_addr
        ether.dst = 'ff:ff:ff:ff:ff:ff'
        ether.ethertype = EtherType.ARP
        arp = Arp(operation=ArpOperation.Request,
            senderhwaddr=self.src_mac_addr,
            senderprotoaddr=self.sourceIP,
            targethwaddr='ff:ff:ff:ff:ff:ff',
            targetprotoaddr=self.destIP)
        arppacket = ether + arp
        return arppacket

    def create_arp_reply(self):
        # Construct an ARP reply packet
        ether = Ethernet()
        ether.src = self.src_mac_addr
        ether.dst = self.dest_mac_addr
        ether.ethertype = EtherType.ARP
        arp = Arp(operation=ArpOperation.Reply,
            senderhwaddr=self.src_mac_addr,
            senderprotoaddr=self.sourceIP,
            targethwaddr=self.dest_mac_addr,
            targetprotoaddr=self.destIP)
        arppacket = ether + arp
        return arppacket
