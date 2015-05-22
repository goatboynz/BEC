# -*- encoding: utf-8 -*-


# Set your config name for your Bec(s) here. 
SERVER1 = "a3.cfg"	# in this example it would be: Bec.exe -f a3.cfg  "my 1st arma3 server"
SERVER2 = "a2.cfg"	# in this example it would be: Bec.exe -f a3_2.cfg  "my 2nd arma3 server"
SERVER3 = "foo.cfg"

# This is the list that contains all servers you want the plugin to run on..
SERVERS = [SERVER1, SERVER2] 

def Servers(config_name):

	# Settings for server1
	if config_name == SERVER1:
		
		# set sample time in sec.
		samptime = 1
		
		# set how long the server will be locked..
		locktime = 3
		
		# set limit of connections.
		consec = 1

		# 1,3,1  meeans, 1 connection per 1 sec will lock server for 3 sec.
		return [samptime, locktime, consec]
		
	elif config_name == SERVER2:
		samptime = 5 
		locktime = 5
		consec = 5
		# 5,5,5 means. 5 connectiosn per 5 sec will lock server for 5 sec.
		return [samptime, locktime, consec]
	
	elif config_name == SERVER3:
		return [1, 5, 2]
	
	else:
		return False