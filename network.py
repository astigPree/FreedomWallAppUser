
import socket
from typing import Union , Optional
import pickle

def convert_to_bytes(data : Union[str ,dict , list ] ) -> bytes :
	if not data:
	       raise ValueError("data is empty")
	return pickle.dumps(data)
    

def convert_to_object(data : bytes ) -> Union[str , list , dict]  :
	if not data:
		raise ValueError("data is empty")
	return pickle.loads(data)

def create_tcp_server_socket(addr : str , port : int , listen = None) -> Union[ tuple[socket.socket , str] , tuple[None , str] ] :
    """
        Create a TCP server socket with the specified address and port.

        Parameters:
        addr (str): The address to bind the socket to.
        port (int): The port to bind the socket to.
        listen (Optional[int]): The maximum number of queued connections. If not provided, the socket listens for connections.

        Returns:
        Union[Tuple[socket.socket, str], Tuple[None, str]]: A tuple containing the socket object and the string 'done' if the socket is created successfully, or None and an error message if an error occurs.
    """
    try :
        server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        server.bind( (addr , port) )
        if listen :
            server.listen(listen)
        else :
            server.listen()
    except OSError as err :
        return (None , str(err))
    else:
        return (server , 'done')

def create_tcp_client_socket(addr : str , port : int ) -> Union[ tuple[socket.socket , str] , tuple[None , str] ] :
    """
        Create a TCP server socket with the specified address and port.

        Parameters:
        addr (str): The address to connect the socket to.
        port (int): The port to connect the socket to.
        
        Returns:
        Union[Tuple[socket.socket, str], Tuple[None, str]]: A tuple containing the socket object and the string 'done' if the socket is created successfully, or None and an error message if an error occurs.
    """
    try :
        server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        server.connect( (addr , port) )
    except OSError as err :
        return (None , str(err))
    else:
        return (server , 'done')

def recieved_data_from(client : socket.socket, byte = 16 , shutdown = False) -> Union[ tuple[object , str] , tuple[None , str]] :
    """
        Receive data from a specified socket and return the data as an object.

        Parameters:
        client (socket.socket): The socket to receive data from.
        byte (int): The maximum number of bytes to be received at a time.
        shutdown (Optional[bool]): Whether to close the socket after the data is received. If not provided, the socket is not closed.

        Returns:
        Union[Tuple[object, str], Tuple[None, str]]: A tuple containing the received data as an object and the string 'done' if the data is received successfully, or None and an error message if an error occurs.
    """
    try:
        datas: list[bytes] = []
        while True:
            data: Optional[bytes] = client.recv(byte)
            if not data:
                break
            datas.append(data)
        return (datas, 'done')
    except (ConnectionRefusedError, ConnectionAbortedError, TimeoutError, BlockingIOError, Exception) as err:
        if shutdown:
            client.close()
        return (None, str(err))


def send_data_to( client : socket.socket , data : bytes , shutdown = False) -> tuple[bool , str] :
    """
        Send data to a specified socket.

        Parameters:
        client (socket.socket): The socket to send data to.
        data (bytes): The data to be sent.
        shutdown (Optional[bool]): Whether to close the socket after the data is sent. If not provided, the socket is not closed.

        Returns:
        Tuple[bool, str]: A tuple containing True and the string 'done' if the data is sent successfully, or False and an error message if an error occurs.
    """
    try :
        client.sendall(data)
    except (BrokenPipeError, ConnectionResetError, TimeoutError, BlockingIOError, Exception) as err:
        return (False, str(err))
    else :
        return ( True , 'done')
    finally:
        if shutdown:
            client.close()


def accept_client( server : socket.socket) -> tuple[ Union[socket.socket , None] , str] :
    try:
        client , addr = server.accept()
    except  ( BlockingIOError , TimeoutError , InterruptedError , Exception ) as err :
        return ( None , str(err))
    else:
        return (client , addr)




	