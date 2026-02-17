from fastapi import FastAPI
from Crypto.Random import get_random_bytes
import base64

app = FastAPI()

# ONE shared mesh key for all nodes
MESH_KEY = base64.b64encode(get_random_bytes(32)).decode()

@app.post("/register")
def register_node(data: dict):
    return {"key": MESH_KEY}


