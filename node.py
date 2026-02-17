import json
import time
import queue
import requests
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import uuid   # NEW

class MeshNode:
    def __init__(self, node_id, cloud_url):
        self.node_id = node_id
        self.cloud_url = cloud_url
        self.neighbors = []
        self.online = True
        self.message_queue = queue.Queue()
        self.seen_packets = set()  # NEW: track processed packets
        self.key = None

        self.register_with_cloud()

    # ----------------------------
    # CLOUD REGISTRATION
    # ----------------------------
    def register_with_cloud(self):
        print(f"[{self.node_id}] Registering with cloud...")
        response = requests.post(f"{self.cloud_url}/register", json={"node_id": self.node_id})
        self.key = base64.b64decode(response.json()["key"])
        print(f"[{self.node_id}] Received encryption key from cloud")

    # ----------------------------
    # ENCRYPTION
    # ----------------------------
    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode()

    def decrypt(self, encrypted_data):
        raw = base64.b64decode(encrypted_data)
        iv = raw[:16]
        ct = raw[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

    # ----------------------------
    # MESH FUNCTIONS
    # ----------------------------
    def add_neighbor(self, neighbor_node):
        self.neighbors.append(neighbor_node)

    def send_message(self, target_id, message, priority="data"):
        encrypted = self.encrypt(message)
        packet = {
            "id": str(uuid.uuid4()),  # NEW: unique packet id
            "from": self.node_id,
            "to": target_id,
            "payload": encrypted,
            "priority": priority
        }
        print(f"[{self.node_id}] Sending packet to mesh...")
        self.forward_packet(packet)

    def forward_packet(self, packet):
        if not self.online:
            print(f"[{self.node_id}] Offline. Queuing packet.")
            self.message_queue.put(packet)
            return

        for neighbor in self.neighbors:
            # Only forward if neighbor is not the sender
            neighbor.receive_packet(packet)

    def receive_packet(self, packet):
        if packet["id"] in self.seen_packets:
            # Already processed this packet, ignore
            return

        self.seen_packets.add(packet["id"])  # Mark as seen

        if not self.online:
            print(f"[{self.node_id}] Offline. Storing packet.")
            self.message_queue.put(packet)
            return

        if packet["to"] == self.node_id:
            decrypted = self.decrypt(packet["payload"])
            print(f"[{self.node_id}] RECEIVED from {packet['from']}: {decrypted}")
        else:
            print(f"[{self.node_id}] Forwarding packet...")
            self.forward_packet(packet)

    def go_offline(self):
        self.online = False
        print(f"[{self.node_id}] Node is now OFFLINE")

    def go_online(self):
        self.online = True
        print(f"[{self.node_id}] Node is now ONLINE")
        self.process_queue()

    def process_queue(self):
        print(f"[{self.node_id}] Processing queued packets...")
        while not self.message_queue.empty():
            packet = self.message_queue.get()
            self.forward_packet(packet)
