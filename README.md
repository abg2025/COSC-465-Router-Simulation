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
- `packet.py`: This deals with how data packets are made and handled.

### Architecture
We designed our network to let multiple routers and clients interact in a controlled setting:
- **Routers** handle packet forwarding based on set rules.
- **Clients** create network traffic by sending and receiving packets.
- **Network Environment** allows communication between clients and routers, similar to how real networks operate.

### Automated Testing
We developed a detailed testing program using Python's `unittest` framework to check if our network simulation works correctly. This includes tests that automatically create packets and make sure they get to the right clients, confirming that our network acts as expected. (WORK IN PROGRESS)

#### Test Scenarios
- **Packet Routing:** We check if packets are routed correctly with direct links according to the network layout specified in `network_config_test.json`.
- **Dynamic Topology Support:** Our tests make sure the simulation can adjust to any network layout, especially those using dynamic routing and direct links. (WORK IN PROGRESS)

To run the tests, use this command:
```bash
python -m unittest test
