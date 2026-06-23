import time
import subprocess
from collections import defaultdict
from threading import Lock
from scapy.all import TCP, IP, sniff
import requests

BACKEND_URL = "http://127.0.0.1:8000/portscan"

THRESHOLD = 10
TIME_WINDOW = 10

blocked_ips : set = set()
flagged_ips : set = set()

connection : dict = defaultdict(list)

lock = Lock()
logs = open("Port_Scanner_log.txt", "a")


def send_to_backend(data : dict) -> None:

	try:
		
		response = requests.post(

			BACKEND_URL,
			json=data
		)
		print(f"[+] Data sent to Backend : {response.status_code}")

	except Exception as e:

		print(f"[-] Error Backend : {e}")

def block_ips(src : str) -> None:

	try:

		subprocess.run(
			["iptables", "-A", "INPUT", "-s", src, "-j", "DROP"],
			check=True
		)

		msg = f"[BLOCKED] {src}\n"

	except subprocess.CalledProcessError as e:

		msg = f"[BLOCK FAILED] {src} - {e}\n"


	print(msg, end="")
	logs.write(msg)
	logs.flush()


def prompt_user(src : str) -> None:

	with lock:

		ports = [p for p, _ in connection[src]]
		payload = {"ip" : src,
			"ports_scanned" : list(ports)
		}

		send_to_backend(payload)

		print(f"[!] Potential port scanner detected : {src}")

		while True:

			choix = input("Block this IP ? (y / n) : ").strip().lower()

			if choix == "y":

				blocked_ips.add(src)
				block_ips(src)
				break;
			elif choix == "n":

				print(f"[INFO] {src} flagged but not blocked.")
				logs.write(f"[FLAGED] {src}\n")
				logs.flush()
				break
			else:

				print("Please enter \"y\" or \"n\".")


def port_scanner(pkt) -> None:

	if not (pkt.haslayer(TCP) and pkt.haslayer(IP)):

		return

	if pkt[TCP].flags != 2:

		return


	src : str = pkt[IP].src
	dport : int = pkt[TCP].dport
	now : float = time.time()

	if src in blocked_ips:

		return

	should_prompt = False
	with lock:

		
		entries = connection[src]
		connection[src] = [(p, t) for p, t in entries if now - t <= TIME_WINDOW]
		entries = connection[src]
		known_ports = {p for p, _ in entries}

		if dport not in known_ports:

			connection[src].append((dport, now))

		distinct_ports = len(connection[src])

		if distinct_ports > THRESHOLD and src not in flagged_ips:

			flagged_ips.add(src)
			should_prompt = True

	if should_prompt:

		prompt_user(src)


def main() -> None:

	interface : str = input("Enter your network inteface (e.g. wlan0) : ").strip()
	print(f"[*] Monitoring traffic on {interface} ..................... (Ctrl-C to stop)")

	try:

		sniff(filter="tcp", prn=port_scanner, iface=interface, store=False)

	except KeyboardInterrupt:

		print("\n[*] Stopping monitor.")

	finally:

		logs.close()

if __name__ == "__main__":

	main()
