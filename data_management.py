"""
Use to manage data in the database
"""
import typing
import uuid
import pickle , json
import os
from cryptography.fernet import Fernet

"""
Logic of secured sending
	- send Fernet key to server
	- send the user need ( encrypted with Fernet key )
	- decrypt the user need in the server 
	- recieve the user need from server ( encrypted with Fernet key from user )
	- decrypt the recived data and use it what ever needs

"""

class DataManager:
	
	__slots__ = ( "__dataholder" , "filename" , "__server_locker" , "__app_locker")
	
	def __init__(self  ):
		self.__app_locker : bytes = Fernet.generate_key()
		self.filename = "oc thoughts.aspre"
		self.__dataholder = { 
			"SERVER ID" : "AstigPre45678" , 
			"APP ID" : "OC4567" , 
			"user id" : str(uuid.uuid4())
			}
	
	def get_my_locker(self) -> bytes :
		return self.__app_locker
	
	def get_encrypted_data(self):
		encryption = Fernet(self.__app_locker)
		return encryption.encrypt(self.get_bytes_data())
	
	def decrypt_data(self , data : bytes) :
		decryption = Fernet(self.__app_locker)
		return decryption.decrypt(data)
	
	def get_bytes_data(self) -> bytes:
		return pickle.dumps(self.__dataholder)
	
	def object_from_bytes(self , data : bytes):
		return pickle.loads(data)
	
	def bytes_from_object(self , data : object ):
		return pickle.dumps(data)
		
	def add_data(self , key : str , values : typing.Union[ str , list , dict , bool , tuple ,bytes ]) :
		if not isinstance(key , str):
			raise ValueError(f"key argument in add_data method is not string : {type(key)}")
		if key in self.__dataholder :
			raise ValueError(f"{key} already exist in the app data")
		self.__dataholder[key] = values
	
	def get_data(self , key : str ):
		if not isinstance(key , str):
			raise ValueError(f"key argument in get_data method is not string : {type(key)}")
		return self.__dataholder.get(key)
	
	def delete_data(self , key : str) :
		if not isinstance(key , str):
			raise ValueError(f"key argument in delete_data method is not string : {type(key)}")
		try :
			del self.__dataholder[key]
		except KeyError :
			return 
	
	def update_data(self , key : str , values : typing.Union[ str , list , dict , bool , tuple ,bytes ]) :
		if not isinstance(key , str):
			raise ValueError(f"key argument in add_data method is not string : {type(key)}")
		if key not in self.__dataholder :
			raise ValueError(f"{key} does not exist in the app data")
		if type(self.get_data(key)) != type(values):
			raise TypeError(f"Can't update if the past values data type is not same : {type(values)}")
		self.__dataholder[key] = values
	
	def get_all_data(self) -> dict :
		return self.__dataholder
	
	def save_to(self , path : str , turnToBytes = False ) :
		if not isinstance(path , str):
			raise ValueError(f"path argument is not string : {type(path)} ")
		if not os.path.exists(path) :
			raise ValueError(f"path argument does not exist : {path}")
		if not os.path.isdir(path) :
			raise ValueError(f"path argument is not a directory : {path} ")
		
		with open( os.path.join( path , self.filename ) , mode="wb" if turnToBytes else "w" ) as file :
			if turnToBytes :
				pickle.dump(obj=self.__dataholder , file=file)
			else :
				json.dump(obj=self.__dataholder , fp=file)
			
		
		
	
if __name__ == "__main__" :
	d = DataManager()
	d.add_data("k" , "g")
	d.update_data("k" , "nice")
	print(d.get_encrypted_data())
	
	
	
	
	