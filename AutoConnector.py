#importing socket module 
import socket 
import os
import re 
import requests

class AutoConnector:

	port = 4343
	host_file_name = "./hosts.txt"
	ip = socket.gethostbyname(socket.gethostname())
	print("my ip: " + ip)
	ip_parts = ip.split(".")
	subnet_mask = ip_parts[0] + "." + ip_parts[1] + "." + ip_parts[2] + "."
	pattern = re.escape(subnet_mask) + r"*"

	def ping(self, addr, port):

		#creates a new socket using the given address family.
		socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		#setting up the default timeout in seconds for new socket object
		socket.setdefaulttimeout(0.001)

		#returns 0 if connection succeeds else raises error
		result = socket_obj.connect_ex((addr,port)) #address and port in the tuple format
		print(addr)
		print(result)
		#closes te object
		socket_obj.close()
		return result == 0

	def find_all_devices(self):
		#hosts = get_devices_from_hosts()
		#print(hosts)
		#print("hosts")
		return self.port_scan()

	def get_devices_from_hosts(self):
		devices = {}
		#check if hosts file exists
		if os.path.isfile(self.host_file_name):
			#open file and check for all ips that start with subnet mask
			with open(self.host_file_name, "r") as host_file:
				for line in host_file.readlines():
					words = line.split(" ")
					if re.match(self.pattern, words[1]):
						print("" +words[0])
						devices[words[0]] = words[1]
		else:
			print("File doesn't exist")
		return devices


	def port_scan(self):
		devices = {}
		me = self.ip_parts[3]
		#ping(subnet_mask + str(100), port)
		for i in range(1,255):
			foreign_ip = self.subnet_mask + str(i)
			if self.ping(foreign_ip, self.port):
				r = requests.get("http://" + foreign_ip + ":" + str(self.port) + "/")
				devices[...] = foreign_ip
		return devices

