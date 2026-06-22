from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth
import datetime
import requests

BACKEND_URL : str = "http://127.0.0.1:8000/deauth"

logs = open("Deauth_Scanner.txt", "a")

def send_to_backend(data : dict) -> None:

	try:

		response = requests.post(

			BACKEND_URL,
			json=data

		)
		print(f"[+] Data sent to Backend : {response.status_code}")

	except Exception as e:

		print(f"[-] Error Backend : {e}")

def deauth_detection(pkt):

	
	if pkt.haslayer(Dot11) and pkt.type == 0 and pkt.subtype == 12:

		timetmp = str(datetime.datetime.now())
		mac = pkt.addr2 if pkt.addr2 else "Unknown"
		msg = f"[{timetmp}] Deauthentication Attack detected against device with MAC address: {mac}"
		#u can add 
		"""data = {
    		"attacker_mac": pkt.addr2,
    		"victim_mac": pkt.addr1,
    		"ap_mac": pkt.addr3 <- acces_point
		}"""


		data = {"mac" : str(mac)}
		send_to_backend(data)

		logs.write(msg + "\n")
		logs.flush()
		print(msg)

def main():

	interface = input("Please entre your interface : ")
	print("Monitoring traffic .......")
	sniff(prn=deauth_detection, iface=interface, store=0)
	#store = 0 means that Packets are not stored in memory; only passed to callback


if __name__ == '__main__':

	main()
