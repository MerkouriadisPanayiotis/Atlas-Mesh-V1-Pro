# =====================================
# AtlasMesh v1 PRO Terminal UI 
# =====================================

from node import MeshNode
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from time import sleep

console = Console()

# ----------------------------
# Node colors
# ----------------------------
NODE_COLORS = {
    "A": "cyan",
    "B": "magenta",
    "C": "yellow"
}

# ----------------------------

# ----------------------------
def show_banner():
    banner_text = r"""
 █████╗ ████████╗██╗      █████╗ ███████╗    ███╗   ███╗███████╗███████╗██╗  ██╗
██╔══██╗╚══██╔══╝██║     ██╔══██╗██╔════╝    ████╗ ████║██╔════╝██╔════╝██║  ██║
███████║   ██║   ██║     ███████║███████╗    ██╔████╔██║█████╗  ███████╗███████║
██╔══██║   ██║   ██║     ██╔══██║╚════██║    ██║╚██╔╝██║██╔══╝  ╚════██║██╔══██║
██║  ██║   ██║   ███████╗██║  ██║███████║    ██║ ╚═╝ ██║███████╗███████║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
    """
    panel = Panel(
        f"[#D2B48C]{banner_text}[/#D2B48C]",
        title="[bold #D2B48C]ATLAS MESH[/bold #D2B48C]",
        expand=False,
        border_style="#D2B48C"
    )
    console.print(panel)
    console.print("Initializing Mesh Network", end="")
    for _ in range(5):
        console.print(".", end="")
        sleep(0.3)
    console.print(" [bold green]Done![/bold green]\n")
    sleep(0.5)

# ----------------------------
#  Initialize Nodes
# ----------------------------
CLOUD_URL = "http://localhost:8000"

nodeA = MeshNode("A", CLOUD_URL)
nodeB = MeshNode("B", CLOUD_URL)
nodeC = MeshNode("C", CLOUD_URL)

# Bi-directional mesh neighbors
nodeA.add_neighbor(nodeB)
nodeB.add_neighbor(nodeC)
nodeB.add_neighbor(nodeA)
nodeC.add_neighbor(nodeB)

# ----------------------------
# Live Status Table Function
# ----------------------------
def display_status(highlight_packet=None, active_nodes=[]):
    table = Table(title="AtlasMesh Node Status")
    table.add_column("Node", style="bold")
    table.add_column("Online", style="bold")
    table.add_column("Queue Depth", style="bold")
    table.add_column("Last Message", style="bold")

    nodes = [nodeA, nodeB, nodeC]
    for n in nodes:
        color = NODE_COLORS.get(n.node_id, "white")
        online_status = f"[{color}]🟢 Online[/{color}]" if n.online else f"[red]🔴 Offline[/red]"
        last_msg = highlight_packet.get(n.node_id, "") if highlight_packet else ""
        # Highlight active nodes
        if n.node_id in active_nodes:
            online_status = f"[bold {color} on yellow]ACTIVE[/bold {color} on yellow]"
        table.add_row(n.node_id, online_status, str(n.message_queue.qsize()), last_msg)
    return table

# ----------------------------
# Animated Message Flow 
# ----------------------------
def animate_message_flow(packet):
    path = []
    if packet["from"] == "A" and packet["to"] == "C":
        path = ["A", "B", "C"]
    else:
        path = [packet["from"], packet["to"]]

    flow_text = ""
    for i, node_id in enumerate(path):
        flow_text += f"→ [{NODE_COLORS.get(node_id,'white')}]{node_id}[/{NODE_COLORS.get(node_id,'white')}] "
        console.print(flow_text)
        sleep(0.3)

# ----------------------------
# 
# Show Banner
# ----------------------------
show_banner()

# ----------------------------
# Main Loop
# ----------------------------
highlight_packet = {}  # Last messages per node

with Live(display_status(highlight_packet), refresh_per_second=2, console=console) as live:
    while True:
        #  menu panel
        menu_panel = Panel.fit(
            "[bold #D2B48C]Menu:[/bold #D2B48C]\n"
            "[1] Send message A -> C\n"
            "[2] Take B Offline\n"
            "[3] Bring B Online\n"
            "[4] Exit",
            title="[bold #D2B48C]AtlasMesh Controls[/bold #D2B48C]",
            border_style="#D2B48C"
        )
        live.stop()  # pause live table while input
        console.print(menu_panel)
        choice = console.input("[bold cyan]Select:[/bold cyan] ").strip()
        live.start()  # resume live table

        if choice == "1":
            live.stop()
            msg = console.input("Enter message: ")
            live.start()
            nodeA.send_message("C", msg, priority="voice")
            # Animate message through nodes
            for active in ["A", "B", "C"]:
                live.update(display_status(highlight_packet, active_nodes=[active]))
                sleep(0.3)
            animate_message_flow({"from": "A", "to": "C"})
            highlight_packet["C"] = f"[bold green]{msg}[/bold green]"

        elif choice == "2":
            nodeB.go_offline()
            highlight_packet["B"] = "[red]OFFLINE[/red]"

        elif choice == "3":
            # Bring B online and deliver queued messages
            nodeB.go_online()
            highlight_packet["B"] = "[green]ONLINE[/green]"
            while not nodeB.message_queue.empty():
                packet = nodeB.message_queue.get()
                # Animate queued message
                for active in ["A", "B"]:
                    live.update(display_status(highlight_packet, active_nodes=[active]))
                    sleep(0.3)
                animate_message_flow(packet)
                highlight_packet[packet["to"]] = f"[bold green]{packet['payload']}[/bold green]"
                live.update(display_status(highlight_packet))
                sleep(0.3)

        elif choice == "4":
            console.print("[bold red]Exiting AtlasMesh...[/bold red]")
            break

        else:
            console.print("[bold red]Invalid selection![/bold red]")

        live.update(display_status(highlight_packet))
        sleep(0.1)
