
from network import NetworkTransaction

from threading import Thread
import socket , pickle , sys

ip = ( "localhost" , 45678)
test_data = { "gwapo" : "200"*100}
print("Size : " , sys.getsizeof(test_data))
print("Pickle Size : ", sys.getsizeof(pickle.dumps(test_data)))


def recievingFunction(client : socket.socket) :
	try :
		datas = []	
		while True :
			data = client.recv(16)
			if not data :
				break
			datas.append(data)
	except OSError :
		print("Error")
	else :
		print(pickle.loads(b"".join(datas)))
	finally :
		client.close()

def clientTest():
	client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
	client.connect(ip)
	client.send(pickle.dumps(test_data))
	client.close()

def serverTest():
	server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
	server.bind(ip)
	server.listen(1)
	
	client , _ = server.accept()
	recievingFunction(client)
	server.close()

def serverTest2():
	server = NetworkTransaction()
	server.create_server()
	client , addr = server.server.accept()
	data = server.recieved_data_from(client)
	print(server.object_from(b"".join(data)))
	
if __name__ == "__main__" :
	Thread(target=serverTest2).start()
	Thread(target=clientTest).start()