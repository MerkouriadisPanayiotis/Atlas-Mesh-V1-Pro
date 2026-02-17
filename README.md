# 🛰️ AtlasMesh v1
> **Terminal-based Autonomous Mesh Network Simulator**

[![Python Version](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

AtlasMesh v1 is a terminal-based autonomous mesh network simulator that demonstrates the core concepts of decentralized communication, message queuing, and node coordination.

---

## 📖 Overview
AtlasMesh allows users to visualize how autonomous mesh networks operate in a controlled, offline environment. It mimics real-world principles useful for disaster recovery, IoT networks, and decentralized messaging systems.

### Core Capabilities
* **Self-Healing Routing:** Messages automatically reroute if a node is offline.
* **Offline Message Queueing:** Messages are stored and delivered automatically once the node comes online.
* **Topology Awareness:** Nodes forward messages intelligently based on network status.
* **Autonomous Packet Forwarding:** Simulates real-world packet forwarding with confirmation of delivery.

---

## 🛠️ Installation & Setup

1. **Navigate to the project:**
   ```bash
   cd AtlasMesh
Create and enter Virtual Environment:

Windows: python -m venv venv then venv\Scripts\activate

Mac/Linux: python3 -m venv venv then source venv/bin/activate

Install dependencies:

Bash
pip install -r requirements.txt
Install Cloud Server dependencies:

Bash
cd cloud_server
pip install -r requirements.txt
⚡ How to Run
Step 1: Start the Cloud Server

From the cloud_server folder, run:

Bash
uvicorn server:app --reload
KEEP THIS TERMINAL TAB OPEN.

Step 2: Run the Mesh Simulation

OPEN A NEW TERMINAL WINDOW.

Navigate to the project: cd AtlasMesh

Activate the venv:

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

Start the simulation:

Bash
python mesh_sim.py

Usage Instructions
Once active, use the menu to control the simulation:

[1],Send Message,Send a packet from Node A to Node C.
[2],Take B Offline,Simulates hardware failure; triggers message queuing.
[3],Bring B Online,"Revives node; triggers ""Self-Healing"" and queue flush."
[4],Exit,Safely shuts down the simulation.