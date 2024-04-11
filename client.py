from switchyard.lib.userlib import *

class Client:
    def __init__(self, net, ip, mac, name):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.net = net
    
    