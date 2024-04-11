from switchyard.lib.userlib import *
import router
import json

class JSON:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_network_config(self):
        with open(self.file_path, 'r') as file:
            config = json.load(file)
        return config
    
class Simulation:
    def __init__(self, net, config) -> None:
        pass

def setup_network(self, net, config):
    # Initialize routers based on the JSON config
    routers = {}
    for router_info in config.get('routers', []):
        interfaces = {intf['name']: (intf['ip'], intf['mask'], intf['mac']) for intf in router_info['interfaces']}
        routers[router_info['id']] = router.Router(net, interfaces)

    # Example of initializing client behavior
    clients = {}
    for client_info in config.get('clients', []):
        clients[client_info['id']] = client_info['ip']
        # client logic 
    return routers, clients
    
def main(net):
    # Load and parse the JSON configuration
    json_file = JSON("network_config_test.json")
    config = json_file.load_network_config()
        
    # Setup the network based on the JSON configuration
    setup_network(net, config)
    
    my_interfaces = net.interfaces() 
    mymacs = [intf.ethaddr for intf in my_interfaces]

    while True:
        try:
            timestamp,dev,packet = net.recv_packet()
        except NoPackets:
            continue
        except Shutdown:
            return

    net.shutdown()

