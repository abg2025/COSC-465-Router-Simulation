### Capstone Project Spring 24 COSC 465

## Overview
In this project, we built a network simulation using custom Python classes. Initially, we wanted to use Switchyard to create our network, but we had trouble downloading the correct version. As a result, we decided to make our own network simulation. This change helped us learn a lot about how networks behave by actually building and adjusting our simulation.

## Learning Objectives
Through this project, we managed to:
* Learn how to use object-oriented programming in Python to mimic network activities.
* Gain hands-on experience with simulating routers, clients, and data packets.
* Improve our skills in carefully checking for errors and solving problems in network settings.

## Getting Started
To begin with our simulation, clone our repository and make sure Python is installed on your computer, as it's needed to run the simulation scripts.

## Network Simulation Details
- `router.py`: This simulates how routers manage and forward packets.
- `client.py`: This simulates a network client creating and receiving packets.
- `network.py`: This manages the overall setup and how routers and clients interact.
- `packet.py`: This deals with how data packets are made and handled. Every packet has a
- `test.py`: This deals with initalizing the network and checking to see if network can handle 

### Architecture
We designed our network to let multiple routers and clients interact in a controlled setting:
- **Routers** handle packet forwarding based on set rules.
    1. If packet destination is to another subnet, router sends packet via network layer by finding dest_ip (Network Address) and sending it to the next hop IP, found in the routing table. 
    2. If packet destination is within subnet of router IP, router will check its ARP table (IP to MAC) since packet is sent over the data layer. If the key doesn't exist it will send a ARP request that will be broadcasted to all devices over the subnet. 
- **Clients** create network traffic by sending and receiving packets.
    1. Client will only ever send packet to its gateway IP via the data layer. If gateway ip is not in ARP table it will create an ARP request and broadcast across all devices in the subnet
- **Network Environment** allows communication between clients and routers, similar to how real networks operate.

### Automated Testing
We developed a detailed testing program using Python's `unittest` framework to check if our network simulation works correctly. This includes tests that automatically create packets and make sure they get to the right clients, confirming that our network acts as expected. 

### Test Scenarios
- **Packet Routing:** We check if packets are routed correctly with direct links according to the network layout specified in `network_config_test.json`.
- **Dynamic Topology Support:** Our tests make sure the simulation can adjust to any network layout, especially those using dynamic routing (RIP using Distance Vector Routing) and direct links. The layout was specified in `network_config_dynamic.json`
-  **Same Network Packet Sending:** Our tests make sure the simulation can adjust to multiple clients connected to the same router via network address. The layout was specified in `network_config_1router.json`.
- **Create Your Own Network Test:** To create your own test using the unittest library add a new function within the TestNetworkSimulation class. If you want to test to see if a router or client recieved a specific packet, you can access their recieved_packets property and assertTrue to see if the device ever recieved it. You can also create your own network topologies by creating a new json file. Make sure to follow this template: 
```json
{
    "routers": [
      {
        "name": "Router(num)",
        "ip": "",
        "mask": "/24", 
        "mac_addr": ""
      }
    ],
    "clients": [
      {
        "name": "Client(capital letter)",
        "ip": "",
        "gateway": "Router IP",
        "mac_addr": ""
      },
      
    ],
    "links": [
        {"from": "Router IP", "to": "Other Router IP"}
    ]
  }
```
Make sure that the names of both clients and routers are different for when you add more. Clients gateway must be on the same network address as the router you want to add it to. Mask must be /24 and if you have multiple routers, you need to make sure that the router is atleast connected to one other router on the network using the links. The routers in this simulation are connected via direct links. 


To run the tests, use this command:
```bash
python3 -m unittest test
```

### Challenges and Limitations
- One problem we discovered with using functions to act as our sending packets, was we were getting recursion errors. The same function within classes would be called multiple times, creating this infinite loop. To stop this, we added `recieved_packets` list in client and router so that if the specific packet was already sent to the device, we would immiedately return in the devices `recieve_packet()` function. While this solved our problem, if we ever wanted to implement ACKs in our direct links protocol, our network simulation will not be able to handle those. 
- One limitation of our network is that it is not exactly scalable since we're using RIP as our routing protocol. 
- Another limitation is that our network isn't exactly realistic since we dont ever have any latency with packet transmission over the network. Some of the functions have a time.sleep(1) since it required to wait for table to be updated so that it can resend a packet. 
