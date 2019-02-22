#importing socket module 
import socket 
import os
import re 
import requests
from threading import Thread
import json

class AutoConnector(Thread):

	port = 43432
	host_file_name = "./hosts.json"
	ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

	print("my ip: " + ip)
	ip_parts = ip.split(".")
	subnet_mask = ip_parts[0] + "." + ip_parts[1] + "." + ip_parts[2] + "."
	pattern = re.escape(subnet_mask) + r"*"

	def __init__(self, orchestrator):
		super().__init__()
		self.orchestrator = orchestrator


		#setting up the default timeout in seconds for new socket object


	def ping(self, addr, port):
		#creates a new socket using the given address family.
		socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		socket.setdefaulttimeout(0.2)
		#returns 0 if connection succeeds else raises error
		result = socket_obj.connect_ex((addr,port)) #address and port in the tuple format
		#closes te object
		socket_obj.close()
		return result == 0

	def run(self):
		print("Started auto connector")
		print("reading hosts file")
		hosts = self.get_devices_from_hosts()
		self.orchestrator.update_devices(hosts)
		print(hosts)

		ips_last_parts = [int(ip.split(".")[3]) for ip in hosts.values()]
		print("Connecting to already known devices")
		self.port_scan(ips_last_parts)
		# self.port_scan([86,121])
		rng = list(set(range(0,255)) - set(ips_last_parts))

		print("Searching for new devices...")
		devices = self.port_scan(rng)
		# devices = self.port_scan(range(1,255))

		print(devices)
		self.orchestrator.update_devices(devices)
		self.append_new_devices(devices,hosts)
		return

	def get_devices_from_hosts(self):
		devices = {}
		#check if hosts file exists
		if os.path.isfile(self.host_file_name):
			with open(self.host_file_name, 'r') as fp:
				data = json.load(fp)
				for k,v in data.items():
					#open file and check for all ips that start with subnet mask
					if re.match(self.pattern, v):
						print(k)
						devices[k] = v
		else:
			print("File doesn't exist")

		return devices

	def port_scan(self, ips):
		devices = {}
		me = self.ip_parts[3]
		#ping(subnet_mask + str(100), port)
		#for i in range(20,255):
		for i in ips:
			foreign_ip = self.subnet_mask + str(i)
			payload = {'ip': self.ip, 'port': 5000}
			print("ping to " + foreign_ip)
			if self.ping(foreign_ip, self.port):
				print("Open connection " + foreign_ip)
				r = requests.post("http://" + foreign_ip + ":" + str(self.port) + "/", data=payload)
				device_name = r.content.decode("utf-8")
				devices[device_name] = foreign_ip
		print("Finished port scan")
		return devices

	def append_new_devices(self, devices, old_devices):
		new_devices = {**devices, **old_devices}
		print("New devices")
		print(new_devices)
		with open(self.host_file_name, 'w') as fp:
			json.dump(new_devices, fp)

