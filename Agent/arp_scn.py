import sys
from datetime import datetime
from scapy.all import srp, Ether, ARP, conf
import json
import os
import requests


BACKEND_URL = "http://127.0.0.1:8000/arp" 

def send_to_backEnd(ip_mac):

	try:

		response = requests.post(
			BACKEND_URL,
			json=ip_mac

		)

		print(f"\n [*] Sent to BackEnd -> {response.status_code}")

	except Exception as e:
		print(f"\n [-] Failed to send to BackEnd : {e}")


#Fonction pour Scanner les apparile avec arp protocole

def arp_scanner(interface, ips):
	
	
	print("Scaning ............")
	start_time = datetime.now()

	start_time_scan = start_time.strftime("%H:%M:%S")
	print(f"Time started Scann : {start_time_scan}")
	#Met scapy output silenceux
	conf.verb = 0
	print(f"Interface: {interface}")
	print(f"Target range: {ips}")
	#ans = answer request et unans = unanswer request
	#on va cree un ethernet borodcast france avec ff:ff... pour dire qu'on va lenvoier pour tous les machine dans le reseux
	#srp = send and receve paquetes
	#ARP() ca veux dire cree un arp requeste avec le protocol de distination c'est les ip taget
	
	ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst = ips), timeout = 2, iface=interface, inter=0.1)
	print("\n [*] IP   ------->   MAC")
	results = []


	for snd, rcv in ans:
		ip_mac = {
			"ip" : rcv.psrc,
			"mac" : rcv.hwsrc

		}

		send_to_backEnd(ip_mac)

		results.append(ip_mac)

		print(rcv.sprintf(r"%ARP.psrc%       %Ether.src%"))

	stop_time = datetime.now()
	total_time = stop_time -start_time
	print("\n [*] Scan complet duration : ", total_time)
	
	output = {

		"Start of scan time" : str(start_time),
		"duration" : str(total_time),
		"results" : results

	}

	fileName = "ArpScannerOutput.json"
	if os.path.exists(fileName):
		
		with open(fileName, "r") as f:

			try:

				data = json.load(f)
				
				if not isinstance(data, list):
					data = [data]

			except json.JSONDecodeError:
				data = []


	else:

		data = []

	data.append(output)
	
	with open(fileName, "w") as f:

		json.dump(data, f, indent=4)


	print("\n [*] Results saved in \"ArpScannerOutput.json\" \n")


if __name__ == "__main__":
	
	if len(sys.argv) != 3:

		print(f"Usage : python3 {sys.argv[0]} <interface> <network ip range>")
		sys.exit(1)


	arp_scanner(sys.argv[1], sys.argv[2])
