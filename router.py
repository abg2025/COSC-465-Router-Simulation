import heapq
from packet import Packet 
import ipaddress

class Router:
    def __init__(self, name, ip, mask, mac_addr, network):
        # initialize router attributes
        self.name = name # router name
        self.ip = ip # router ip address
        self.mask = mask # subnet mask
        self.mac_addr = mac_addr # mac address
        self.network = network # reference to the network
        self.routing_table = [] # routing table
        self.arp_table = {} #arp table
        self.ospf_neighbors = set()  # OSPF neighbors
        self.lsdb = {}  # Link State Database

    def receive_packet(self, packet):
        # handle incoming packets based on their types
        if packet.packet_type == 'ARP':
            self.handle_arp_reply(packet)
        elif packet.packet_type == 'IP':
            self.handle_ip(packet)
        elif packet.packet_type == 'OSPF':
            self.handle_ospf_packet(packet)

    def handle_arp_reply(self, packet):
        # handle arp reply packets
        if packet.payload['operation'] == 'request':
            # send arp reply back
            arp_reply = Packet(self.ip, self.mac_addr, packet.source_ip, packet.src_mac_addr, 'ARP', {'operation': 'reply'})
            self.network.send_packet(arp_reply)
            # update arp table with the sender's ip and mac addresses
            self.arp_table[packet.source_ip] = packet.src_mac_addr
        elif packet.payload['operation'] == 'reply':
            # update arp table with the sender's ip and mac addresses
            self.arp_table[packet.source_ip] = packet.src_mac_addr
        
    def is_ip_in_subnet(self, ip1, ip2):
        # check if ip1 is in the same subnet as ip2
        ip1 = ipaddress.ip_address(ip1)
        ip2 = ipaddress.ip_address(ip2)
        return ip1 in ip2

    def handle_ip(self, packet):
        # handle ip packets
        destination = packet.dest_ip
        # check if destination mac address is known
        if not self.arp_table[destination]:
            # if destination is in the same subnet, perform arp request
            if self.is_ip_in_subnet(destination, self.ip + self.mask):
                self.perform_arp_request(self, destination)
                # check if destination ip is in the routing table
        for route in self.routing_table:
            if destination == route['dest_ip']:
                next_hop_ip = route['next_hop_ip']
                next_hop_mac = self.network.resolve_mac(next_hop_ip)
                # update packet with next hop mac address
                packet.dest_mac_addr = next_hop_mac
                packet.src_mac_addr = self.mac_addr
                # send packet to the next hop
                self.network.send_packet(packet, next_hop_mac)
                return
        print("No route found for IP: {}".format(destination))
    
    def perform_arp_request(self, dest_ip):
        # perform arp request for the destination ip
        arp_request = Packet(self.ip, self.mac_addr, dest_ip, 'FF:FF:FF:FF:FF:FF', 'ARP', {'operation': 'request'})
        self.network.send_packet(arp_request)

    def handle_ospf_packet(self, packet):
        # handle OSPF packets
        if packet.payload['type'] == 'Hello':
            self.process_ospf_hello(packet)
        elif packet.payload['type'] == 'LSA':
            self.process_ospf_lsa(packet)

    def process_ospf_hello(self, packet):
        # process OSPF hello packets
        neighbor_ip = packet.source_ip
        # add the neighbor to the OSPF neighbors set
        if neighbor_ip not in self.ospf_neighbors:
            self.ospf_neighbors.add(neighbor_ip)
            # Send OSPF Hello packet back to neighbor
            hello_packet = Packet(self.ip, self.mac_addr, neighbor_ip, neighbor_ip, 'OSPF', {'type': 'Hello'})
            self.network.send_packet(hello_packet)

    def process_ospf_lsa(self, packet):
        # process OSPF link state advertisement (lsa) packets
        lsa_info = packet.payload['lsa_info']
        # update the lsdb with the receieved lsa information
        self.lsdb[lsa_info['lsa_id']] = lsa_info
        # update the routing table based on the lsdb
        self.update_routing_table()

    def update_routing_table(self):
        # Dijkstra's algorithm implementation to update routing table
        graph = self.construct_graph()
        shortest_paths = self.dijkstra(graph)
        self.routing_table = shortest_paths

    def construct_graph(self):
        # construct graph for Dijkstra's algorithm
        graph = {}
        for neighbor_ip in self.ospf_neighbors:
            if neighbor_ip in self.lsdb:
                for dest_ip, cost in self.lsdb[neighbor_ip].items():
                    graph.setdefault(self.ip, []).append((dest_ip, cost))
        return graph

    def dijkstra(self, graph):
        # Dijkstra's algorithm to find shortest paths
        shortest_paths = []
        visited = set()
        queue = [(0, self.ip, [])]  # (cost, node, path)
        
        while queue:
            cost, node, path = heapq.heappop(queue)
            if node not in visited:
                visited.add(node)
                path.append(node)
                shortest_paths.append({'dest_ip': node, 'next_hop_ip': node, 'cost': cost})
                if node in graph:
                    for dest_ip, cost in graph[node]:
                        if dest_ip not in visited:
                            heapq.heappush(queue, (cost, dest_ip, path[:]))
        return shortest_paths

    def flood_ospf_lsa(self, packet):
    # Flood the LSA to OSPF neighbors only
        for neighbor_ip in self.ospf_neighbors:
            neighbor_router = self.network.get_router_by_ip(neighbor_ip)
            if neighbor_router:
                lsa_packet = Packet(self.ip, self.mac_addr, neighbor_ip, self.arp_table.get(neighbor_ip, 'FF:FF:FF:FF:FF:FF'), 'OSPF', {'type': 'LSA', 'lsa_info': packet.payload['lsa_info']})
                self.network.send_packet(lsa_packet)
    
    def initialize_ospf(self):
        # initialize OSPF by sending Hello packets to discover neighbors
        for device_name, device in self.network.devices.items():
            if isinstance(device, Router) and device.name != self.name:
                hello_packet = Packet(self.ip, self.mac_addr, device.ip, 'FF:FF:FF:FF:FF:FF', 'OSPF', {'type': 'Hello'})
                self.network.send_packet(hello_packet)

           
