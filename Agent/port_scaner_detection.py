import time
import subprocess
from collections import defaultdict
from threading import Lock
from scapy.all import TCP, IP, sniff
import requests


BACKEND_URL = "http://127.0.0.1:8000/portscan"

THRESHOLD = 10   # Number of distinct ports before flagging
TIME_WINDOW = 10  # Sliding window in seconds

blocked_ips: set = set()
flagged_ips: set = set()

# Maps src_ip -> list of (port, timestamp) tuples
connection: dict = defaultdict(list)

lock = Lock()  # Protect shared state from race conditions
logs = open("Port_Scanner_log.txt", "a")

def send_to_backend(data : dict) -> None:

	try:

		reponse = requests.post(

			BACKEND_URL,
			json=data
		)

		print(f"[+] Data sent to Backend : {reponse.status_code}")

	except Exception as e:

		print(f"[-] Error Backend : {e}")


def block_ip(src: str) -> None:
    """Apply an actual firewall rule via iptables."""
    try:
        subprocess.run(
            ["iptables", "-A", "INPUT", "-s", src, "-j", "DROP"],
            check=True
        )
        msg = f"[BLOCKED] {src}\n"
    except subprocess.CalledProcessError as e:
        msg = f"[BLOCK FAILED] {src} — {e}\n"
    print(msg, end="")
    logs.write(msg)
    logs.flush()
	

def prompt_user(src: str) -> None:
    """Ask the operator whether to block the flagged IP."""


    with lock:
	ports = [p for p, _ in connection[src]]

	payload = {"ip" : src,
		"ports_scanned" : list(ports)
	}


    send_to_backend(payload)


    print(f"\n[!] Potential port scanner detected: {src}")
    while True:
        choice = input("Block this IP? (y / n): ").strip().lower()
        if choice == "y":
            blocked_ips.add(src)
            block_ip(src)
            break
        elif choice == "n":
            print(f"[INFO] {src} flagged but not blocked.")
            logs.write(f"[FLAGGED, NOT BLOCKED] {src}\n")
            logs.flush()
            break
        else:
            print('Please enter "y" or "n".')


def port_scanner(pkt) -> None:
    # Only care about SYN packets (new connection attempts)
    if not (pkt.haslayer(TCP) and pkt.haslayer(IP)):
        return
    if pkt[TCP].flags != "S":
        return

    src: str = pkt[IP].src
    dport: int = pkt[TCP].dport
    now: float = time.time()

    # Silently drop packets from already-blocked IPs
    if src in blocked_ips:
        return

    sould_prompt = False
    with lock:
        entries = connection[src]

        # --- Sliding window: drop entries older than TIME_WINDOW ---
        connection[src] = [(p, t) for p, t in entries if now - t <= TIME_WINDOW]
        entries = connection[src]

        # Add this port only if not already seen in the current window
        known_ports = {p for p, _ in entries}
        if dport not in known_ports:
            connection[src].append((dport, now))

        distinct_ports = len(connection[src])

        # Flag only once per source
        if distinct_ports > THRESHOLD and src not in flagged_ips:
            flagged_ips.add(src)
	    sould_prompt = True
            # Prompt runs on the sniff thread — fine for a CLI tool.
            # For a production daemon, push src onto a Queue and handle
            # in a dedicated UI thread instead.
    if sould_prompt:
   	 prompt_user(src)


def main() -> None:
    interface: str = input("Enter your network interface (e.g. eth0): ").strip()
    print(f"[*] Monitoring traffic on {interface} …  (Ctrl-C to stop)")
    try:
        sniff(filter="tcp", prn=port_scanner, iface=interface, store=False)
    except KeyboardInterrupt:
        print("\n[*] Stopping monitor.")
    finally:
        logs.close()


if __name__ == "__main__":
    main()
