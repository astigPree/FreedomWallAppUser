"""
Use to manage data in the database
"""

import sqlite3

def create_database( path: str , table : str , cols : list[str, ...] , types : [str, ...] , unique_id : bool ) -> str :
	"""
	IT CREATE A DATABASE
path : str = directory and filename of the database file
table : str = name of the table 
cols : list of str = columns in the table
types : list of str = types of every column
unique_id : bool = if has a ID or not 
	"""
	if len(cols) != len(types) :
		return f"Not correct size of cols : {len(cols)} and types : {len(types)}"
	
	command = f"CREATE TABLE IF NOT EXISTS {table} ("
	if unique_id :
		command += " id INTEGER PRIMARY KEY ,"
	for i in range(len(cols)) :
		command += f" {cols[i]} {types[i]} ,"
	command = command[:-1] + ")"
	
	conn = sqlite3.connect(path)
	cursor = conn.cursor()
	try :
		cursor.execute(command)
	except ( sqlite3.OperationalError, sqlite3.Error ) as err :
		return f"Execute error : {err}"
	else :
		return "Done"
	finally :
		conn.commit()
		conn.close()



if __name__ == "__main__" :
	pass