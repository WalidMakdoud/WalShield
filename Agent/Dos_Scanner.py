import sys
import time
from scapy.all import *
from collections import deque
import requests


BACKEND_URL = "http://127.0.0.1:8000/dos"
THRESHOLD = 5000
SLIDING_WINDOW = 30

pkt_counter = {}
#pkt_timestamps = deque()
blocked_ips = set()
flagged_ips = set()



logs = open("Dos_Scanner.txt", "a")


def send_to_backend(data : dict) -> None:

	try:

		response = requests.post(
			BACKEND_URL,
			json=data
		)

		print(f"[+] Data sent to the backend {response.status_code}")

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



def dos_scanner(pkt) -> None:

		
		if IP not in pkt:

			return

		src = pkt[IP].src
		now = time.time()

		if src in blocked_ips or src in flagged_ips:

			return 

		if src not in pkt_counter:

			pkt_counter[src] = deque()

		pkt_counter[src].append(now)
		
		while pkt_counter[src] and pkt_counter[src][0] < now - SLIDING_WINDOW:

			pkt_counter[src].popleft()


		count = len(pkt_counter[src])

		if count > THRESHOLD and src not in flagged_ips:

			valide = False

			while not valide:

				block : str = input("Do u want to block the IP (\"y\" or \"n\") : ").strip().lower()
				
				if block == "y":

					valide = True
					msg = f"[BLOCKED] {src}\n"
					logs.write(msg)
					logs.flush()
					print(msg)
					block_ips(src)
					blocked_ips.add(src)
					flagged_ips.add(src)

				elif block == "n":

					valide = True
					msg = f"[FLAGGED] {src}\n"
					logs.write(msg)
					logs.flush()
					print(msg)
					flagged_ips.add(src)

				else :

					print("Please entre a valide chois.")


def main() -> None:

	interface : str = input("Enter the network interface (e.g. wlan0) : ").strip()
	print(f"[+] Network {interface} monitoring .........")
	sniff(filter="ip", iface=interface, prn=dos_scanner, store=False)


if __name__ == "__main__":

		main()
