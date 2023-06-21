import socket, threading, os, sys

# Server Class
class Server():
	def __init__(self, serv_addr, serv_port, c_dir):
		self.addr = serv_addr
		self.port = serv_port
		self.current_directory = c_dir
		#os._exit(0)

	# the webpage function call this function(read_index) to indentify if either return an index file or a directory listing
	def read_index(self):
		files = [file for root, dirz, file in os.walk(self.current_directory)][0]
		for index in files:
			if(index in ['index.html','index.php']):
				return open(index).read()
			else:
				page = "<html> <head> <meta name='viewport' content='width=device-width, initial-scale=1'> <title>Ninja-PSW - Indexing</title> </head> <style> *{ font-family: sans-serif; } body{ margin:0; height: 100vh; background-color:rgb(0,0,0,0.2); } .banner{ margin-top:10px; } .banner h2{ text-align: center; font-weight: bold; font-size:28px; } .banner p, .items{ margin-left: 15px; font-size:18px; } </style> <body> <div class='banner''> <h2>Simple Web Server</h2> <p>Created by: <a href='https://www.facebook.com/profile.php?id=100085378914881'>Anikin Luke Abales</a></p><hr> </div>"
				for filename in files:
					page+=f"<a class='items' href='{filename}'>{filename}</a><br>"
				page+="</body></html>"
				return page

	# Looping section where webpage is returned/display to the client.
	def webpage(self,srv_sock):
		c_sock, c_addr = srv_sock.accept() # c_sock = client socket, c_addr = client address 
		response = c_sock.recv(1024).decode()
		web_dir = response.split("/")[1]
		web_dir = web_dir.replace(" HTTP","")
		web_file = web_dir.split(".")
		print(web_file[1])
		img_file_types = ['jpg','png','jpeg']

		if(web_dir == ''): # return/display the index file from the "read_index" function.
			index = self.read_index()
			webpage = "HTTP/1.1 200 OK\n\n"+index
			c_sock.sendall(webpage.encode())
			c_sock.close()
		elif(web_file[1] in img_file_types):
			current_file = open(self.current_directory+web_dir).read()
			webpage = f"HTTP/1.0 200 OK\nContent-Type: image/png\nContent-Length: {os.path.getsize(self.current_directory+web_dir)}\n\n{current_file}"
			c_sock.sendall(webpage.encode())
			c_sock.close()
		else:
			try:
				webpage = "HTTP/1.1 200 OK\n\n"+open(self.current_directory+web_dir).read() # Return/display file if it is found in the current/specified server directory
				c_sock.sendall(webpage.encode())
				c_sock.close()
			except Exception as err:
				index = self.read_index()
				webpage = "HTTP/1.1 404 Not Found" #returns 404 if the file is not found in the current/specified server directory
				c_sock.sendall(webpage.encode())
				c_sock.close()

	# It will start the server connection and loop the webserver accessed by clients
	def run(self):
		tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_sock.bind((self.addr,self.port))
		tcp_sock.listen(1)
		while True:
			status = self.webpage(tcp_sock)
			if(status == 'stop'):
				break

# the Argument Class is used to identify the inquired arguments that will be passed to the server class.
class ArgHandler():
	def __init__(self):
		udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		udp_sock.connect(('8.8.8.8',80))
		
		self.IP = udp_sock.getsockname()[0]
		self.PORT = 1337
		self.DIR = './'

	# CIA stands for Check Inquired Argument
	# The CIA function identifies how many argument inquired by the user/server manager.
	def CIA(self):
		count = 0
		try:
			if(sys.argv[1] in ['-h','--help']):
				print(f"Usage:\n python3 {os.path.basename(__file__)} --ip=<ip> --port=<port> --dir=<dir>\n\n -i |--ip = <ip> default = your_local_ip\n -p |--port=<port> default = 1337\n -d | --dir=<dir> default = current directory")
				os._exit(0)

			for i in range(0,6):
				sys.argv[i+1]
				count = i+1
		except Exception as err:
			pass
		return count

	# The Update Argument function is use to identify what argument is pass and what value of a variable need to be change. 
	def update_args(self, num_result):
		for num in range(int(num_result)):
			try:
				if(sys.argv[num+1] in ['-i','--ip']):
					self.IP = sys.argv[num+2]
				elif(sys.argv[num+1] in ['-p','--port']):
					self.PORT = int(sys.argv[num+2])
				elif(sys.argv[num+1] in ['-d','--dir']):
					self.DIR = sys.argv[num+2]
			except:
				pass

	# The main function controls which data will be returned and passed to the Server class.
	def main(self):
		result = self.CIA() # Check Inquired Argument
		if(result == 0):
			return self.IP, self.PORT, self.DIR
		elif(result%2 == 0):
			self.update_args(result)
			return self.IP, self.PORT, self.DIR
		else:
			return self.IP, self.PORT, self.DIR


if(__name__=="__main__"):
	serv_addr, serv_port, serv_dir = ArgHandler().main()
	webserver = Server(serv_addr, serv_port, serv_dir)
	threading.Thread(target=webserver.run).start()
	print(f"{'Serv-Info':=^22}")
	print(f"\nRunning on:\n- IP: {serv_addr}\n- PORT: {serv_port}\n- DIR: {serv_dir}\n")
	print(f"{'Serv-Info':=^22}")

