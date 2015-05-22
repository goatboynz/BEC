# -*- encoding: utf-8 -*-



# Set your config name for your Bec(s) here. 
SERVER1 = "a3.cfg"	# in this example it would be: Bec.exe -f a3.cfg  "my 1st arma3 server"
SERVER2 = "a2.cfg"	# in this example it would be: Bec.exe -f a3_2.cfg  "my 2nd arma3 server"

# This is the list that contains all servers you want the plugin to run on..
SERVERS = [SERVER1, SERVER2] 

def Servers(config_name):

	# Settings for server1
	if config_name == SERVER1:
		
		# Enable ftp uploade. this variable must be: True or False
		Use_Ftp	= True
		
		# Interval in Seconds between each time it will generate a xml file and uploade it if set to do so.
		# Type int
		Interval = 60
		
		# Address to the ftp server, ip or hostname.
		# Type str
		Host = "127.0.0.1"
		
		# Port the ftp server uses.
		# Type int
		Port = 21
		
		# login name to the ftp server.
		# Type str
		User = "nux"
		
		# Login password to the ftp server.
		# Type str
		Password = "1234"
		
		# Location to where the file will be uploaded.
		# Leave this as: None, to set the users homedir for the uploade location.
		# if your host is "ftp://myhost.com" and you want to uploade the file to another dir. "example to a status dir".
		# you set Dir til. Dir = "/status" , remember leading /
		# Type str || None
		#Dir = "/MyStatus"
		Dir	= None

		# Return data for __init__.py
		return [Use_Ftp, Interval, Host, Port, User, Password, Dir]

	
	# Define more servers below if needed!..
	# Settings for Server2 
	elif config_name == SERVER2:
		Use_Ftp		= False
		Interval 	= 60
		Host 		= None
		Port 		= None
		User 		= None
		Password 	= None
		Dir 		= None
		return [Use_Ftp, Interval, Host, Port, User, Password, Dir]

	#elif config_name == SERVER3:
	# ...
	else:
		return False
	
		
	