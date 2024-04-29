### Capstone Project Spring 24 COSC 465

## Overview
In this project, we have implemented a network simulation using custom Python classes. Initially, we planned to utilize Switchyard to model our network. However, due to difficulties in downloading the correct version, we opted to develop our own network simulation framework. This transition allowed us to gain a deeper understanding of network behaviors through hands-on development and customization.

## Learning Objectives
Through this project, we have achieved the following learning objectives:
* Mastered the use of object-oriented programming in Python to simulate network behaviors.
* Gained practical experience in simulating routers, clients, and data packets within a network.
* Developed skills in meticulous error checking and problem-solving within a networked environment.

## Important Tips
* We found it crucial to thoroughly understand each component of our simulation by reading and understanding switchyard before beginning any development. (Even though we didn't use switchyard, our network object was loosely based on it) 
* Starting early and spacing out our work sessions helped us manage the complexity of the project more effectively.
* Regular testing at each stage of development was key to identifying and resolving issues early.

## Getting Started
To get started with our simulation, clone our repository and ensure Python is installed on your system, as it is necessary for running the simulation scripts.

## Network Simulation Details
Our simulation framework includes several components each handling different aspects of the network:
- `router.py`: Simulates the router's functionality of managing and forwarding packets.
- `client.py`: Simulates a network client that generates and receives packets.
- `network.py`: Manages the overall network setup and interactions between routers and clients.
- `packet.py`: Defines how data packets are constructed and handled during network transmission.

### Architecture
We designed our network to support interactions among multiple routers and clients in a controlled simulation environment:
- **Routers** manage packet forwarding based on predefined routing logic.
- **Clients** generate network traffic by sending and receiving packets.
- **Network Environment** facilitates communication between clients and routers, mimicking real-world network dynamics.

### Automated Testing
We have developed a comprehensive testing suite using Python's `unittest` framework to validate the functionality of our network simulation. This suite includes tests that dynamically create packets and verify their correct delivery to the intended clients, ensuring that the network behaves as expected. (WORK IN PROGRESS) 

#### Test Scenarios
- **Packet Routing:** We test that packets created within the simulation are routed correctly according to the network topology defined in `network_config_test.json`.
- **Dynamic Topology Support:** Our tests verify that the simulation can adapt to any provided network topology, particularly focusing on scenarios that use dynamic routing protocols and direct links. This ensures our network simulation is robust and flexible, capable of handling various realistic network environments. (WORK IN PROGRESS) 

To run the tests, execute the following command:
```bash
python -m unittest test



