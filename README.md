# AtlasMesh v1 – Autonomous Mesh Network Simulator

[![Python Version](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

##  Overview

> **AtlasMesh v1** is a terminal-based autonomous mesh network simulator that demonstrates the core concepts of decentralized communication, message queuing, and node coordination.

It simulates a mesh of network nodes (**A, B, C**) that can:
* **Send messages** across nodes using a self-healing routing mechanism.
* **Queue messages** automatically when a node is offline.
* **Deliver queued messages** instantly when nodes come back online.
* **Operate fully offline** without internet, simulating real-world mesh networks.
* **Demonstrate** network topology awareness, message prioritization, and autonomous packet forwarding.

---

##  Features

AtlasMesh v1 simulates a fully autonomous mesh network, demonstrating:

| Feature | Description |
| :--- | :--- |
| **Decentralized Communication** | Nodes forward messages across the mesh without a central server. |
| **Self-Healing Behavior** | Messages automatically reroute if a node is offline. |
| **Offline Message Queueing** | Messages sent to offline nodes are stored and delivered once the node comes online. |
| **Live Node Status** | Tracks which nodes are online, queued messages, and recent message activity. |
| **Message Prioritization** | Simulates real-world packet forwarding with confirmation of delivery. |
| **Topology Awareness** | Nodes know their neighbors and forward messages intelligently. |



---

##  Installation

1. Clone the repository:

git clone https://github.com/MerkouriadisPanayiotis/Atlas-Mesh-V1-Pro
cd AtlasMesh

Create a Python virtual environment

python3 -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

Install dependencies:
pip install -r requirements.txt
cd cloud_server
install -r requirements.txt
install -r requirements.txt
[KEEP THIS TERMINAL OPEN AND OPEN A NEW TERMINAL WINDOW]

cd AtlasMesh
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
Run the simulator:
python mesh_sim.py


 Usage INSTRUCTIONS

You will see the AtlasMesh banner and live node table.
Use the interactive menu:
[1] Send message A -> C
[2] Take B Offline
[3] Bring B Online
[4] Exit
Example workflow:
Take node B offline [2]
Send a message A → C [1]
→ The message will queue at B
Bring node B online [3]
→ The queued message automatically delivers with animated arrows