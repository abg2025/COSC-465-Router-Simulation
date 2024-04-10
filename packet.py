class Packet:
# should have source IP, source Mac address, destination IP, destination IP MAC address,



    def __init__(self,sourceIp,src_mac_addr,destIP,dest_mac_addr):
        self.sourceIP = sourceIp
        self.src_mac_addr = src_mac_addr
        self.destIP = destIP
        self.dest_mac_addr = dest_mac_addr
        

    def getSourceIP(self):
        return self.sourceIP
    
    def getMacAddr(self):
        return self.src_mac_addr
    
    def getDestIP(self):
        return self.destIP 
    
    def getDestMacAddr(self):
        return self.dest_mac_addr