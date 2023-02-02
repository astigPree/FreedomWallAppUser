"""
Use to manage data in the database
"""
import typing
import uuid
import pickle , json
import os

class DataManager:
	
	__slots__ = ( "__dataholder" , "filename")
	
	def __init__(self  ):
		self.filename = "oc thoughts.aspre"
		self.__dataholder = { 
			"SERVER ID" : "AstigPre45678" , 
			"APP ID" : "OC4567" , 
			"user id" : str(uuid.uuid4())
			}
		
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
	data = DataManager()
	data.add_data("k" , "g")
	data.update_data("k" , "nice")
	
	data.save_to(os.getcwd() , turnToBytes=True)
	
	
	
	
	
	