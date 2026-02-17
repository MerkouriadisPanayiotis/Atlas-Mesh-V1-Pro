# =====================================
# AtlasMesh v1 PRO Terminal UI 
# =====================================

from node import MeshNode
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from time import sleep

# Force a minimum width to ensure the ASCII banner doesn't wrap
console = Console(width=100) 

# Tan color constant
TAN = "#D2B48C"

# ----------------------------
# Node colors
# ----------------------------
NODE_COLORS = {
    "A": "cyan",
    "B": "magenta",
    "C": "yellow"
}

# ----------------------------
# Banner and Initialization
# ----------------------------
def show_banner():
    # Corrected ASCII Banner - Raw string
    banner_raw = r"""
 █████╗ ████████╗██╗      █████╗ ███████╗    ███╗   ███╗███████╗███████╗██╗  ██╗
██╔══██╗╚══██╔══╝██║     ██╔══██╗██╔════╝    ████╗ ████║██╔════╝██╔════╝██║  ██║
███████║   ██║   ██║     ███████║███████╗    ██╔████╔██║█████╗  ███████╗███████║
██╔══██║   ██║   ██║     ██╔══██║╚════██║    ██║╚██╔╝██║██╔══╝  ╚════██║██╔══██║
██║  ██║   ██║   ███████╗██║  ██║███████║    ██║ ╚═╝ ██║███████╗███████║██║  ██║
╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝"""
    
    # Use no_wrap=True and a specific style to keep the layout rigid
    banner_text = Text(banner_raw, style=TAN, no_wrap=True)
    
    # Removed extra padding to save horizontal space
    panel = Panel(
        banner_text,
        title=f"[bold {TAN}]ATLAS MESH[/bold {TAN}]",
        expand=False, 
        border_style=TAN,
        padding=(0, 1)
    )
    
    console.print(panel)
    console.print(f"[{TAN}]Initializing Mesh Network[/{TAN}]", end="")
    for _ in range(5):
        console.print(f"[{TAN}]. [/{TAN}]", end="")
        sleep(0.2)
    console.print(" [bold green]Done![/bold green]\n")
    sleep(0.3)

# ---------------------------------------------------------
# EXECUTION START
# ---------------------------------------------------------
show_banner()

CLOUD_URL = "http://localhost:8000"
nodeA = MeshNode("A", CLOUD_URL)
nodeB = MeshNode("B", CLOUD_URL)
nodeC = MeshNode("C", CLOUD_URL)

nodeA.add_neighbor(nodeB)
nodeB.add_neighbor(nodeC)
nodeB.add_neighbor(nodeA)
nodeC.add_neighbor(nodeB)

def display_status(highlight_packet=None, active_nodes=[]):
    table = Table(
        title=f"[bold {TAN}]AtlasMesh Node Status[/bold {TAN}]", 
        border_style=TAN,
        header_style=f"bold {TAN}",
        width=80 # Keeps the table consistent with the banner width
    )
    table.add_column("Node", style="bold", justify="center")
    table.add_column("Online", justify="center")
    table.add_column("Queue Depth", justify="center")
    table.add_column("Last Message")

    nodes = [nodeA, nodeB, nodeC]
    for n in nodes:
        color = NODE_COLORS.get(n.node_id, "white")
        online_status = f"[{color}]🟢 Online[/{color}]" if n.online else f"[red]🔴 Offline[/red]"
        last_msg = highlight_packet.get(n.node_id, "") if highlight_packet else ""
        
        if n.node_id in active_nodes:
            online_status = f"[bold {color} on #4e3b24]ACTIVE[/bold {color} on #4e3b24]"
        
        table.add_row(n.node_id, online_status, str(n.message_queue.qsize()), last_msg)
    return table

# ----------------------------
# Main Loop
# ----------------------------
highlight_packet = {}

with Live(display_status(highlight_packet), refresh_per_second=4, console=console) as live:
    while True:
        menu_panel = Panel.fit(
            f"[bold {TAN}]Menu:[/bold {TAN}]\n"
            "[1] Send message A -> C\n"
            "[2] Take B Offline\n"
            "[3] Bring B Online\n"
            "[4] Exit",
            title=f"[bold {TAN}]AtlasMesh Controls[/bold {TAN}]",
            border_style=TAN
        )
        live.stop()
        console.print(menu_panel)
        choice = console.input(f"[bold {TAN}]Select action: [/bold {TAN}]").strip()
        live.start()

        if choice == "1":
            live.stop()
            msg = console.input(f"[bold {TAN}]Enter message: [/bold {TAN}]")
            live.start()
            nodeA.send_message("C", msg, priority="voice")
            
            for active in ["A", "B", "C"]:
                live.update(display_status(highlight_packet, active_nodes=[active]))
                sleep(0.3)
            
            highlight_packet["C"] = f"[bold green]{msg}[/bold green]"

        elif choice == "2":
            nodeB.go_offline()
            highlight_packet["B"] = "[red]OFFLINE[/red]"

        elif choice == "3":
            nodeB.go_online()
            highlight_packet["B"] = "[green]ONLINE[/green]"
            while not nodeB.message_queue.empty():
                packet = nodeB.message_queue.get()
                for active in ["A", "B"]:
                    live.update(display_status(highlight_packet, active_nodes=[active]))
                    sleep(0.3)
                highlight_packet[packet["to"]] = f"[bold green]{packet['payload']}[/bold green]"
                live.update(display_status(highlight_packet))
                sleep(0.3)

        elif choice == "4":
            console.print("[bold red]Exiting AtlasMesh...[/bold red]")
            break

        live.update(display_status(highlight_packet))
        sleep(0.1)