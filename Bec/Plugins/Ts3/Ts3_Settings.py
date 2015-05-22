# -*- encoding: utf-8 -*-
#
# Running Multiple Servers but do not want to have all bec's connected to same Ts3 Server?
# Well. as long as you know the config file name using with bec. you would also know what ts3 server to connect to.
# Look at the example below. 3 different config files. so we can set different values for each Ts3 Query Connection.



##
#
# Note !!!..
# > You should not connect to the same Ts3 server with the same Queryname for N Bec instances, you should do as the example below.
#
##



# These variables are to tell the Ts3 plugin which settings to use for the different server querys.
SERVER1 = "a3.cfg"					# This would be for my 1st arma3 server, Bec.exe -f a3.cfg 
SERVER2 = "a2.cfg"					# This would be for my arma2 server, Bec.exe -f a2.cfg 
SERVER3 = "foobar.cfg"				# This would be starting bec as, Bec.exe -f foobar.cfg

# list of config names that will be used in the __init__ file
SERVERS = [ SERVER1, SERVER2 ]

#
# You will also need to create a code block for each server. as seen below. "uncomment them out if needed"
#
def Ts3Servers(config_name):
	'''config_name : this is the name of the config file Bec is started up with.'''

	if config_name == SERVER1:  # or use if config_name == SERVERS[0] or if config_name == "YourConfig.cfg"

		Host 								= "127.0.0.1"	# change if needed
		Port								= 10011
		User								= "serveradmin"
		Password							= "SLMufyy9"	# Change this
		VirtualServer						= 1
		Queryname							= "ArmA3_becObot" # Change this
		ClientRequiredTs3 					= True	# if you want to force players on the ts3 server. warnings will be sent ingame. not in lobby.
		ClientRequiredTs3_Warnings			= 3
		ClientRequiredTs3_KickMessage 		= "Why oh why did you not just connect to the Ts3 Server"
		ClientRequiredTs3_WarningMessage	= "Please connect to our Ts3 Server to play here"
		ClientRequiredTs3_Channel			= ["1", "2"]
		Triggerword 						= "!ts"
		Admins = {
			'OmIZoqKMye9L1GeBo0EULv4LdqY=' : ["nux", 1 ,1, 1 , 1],
			'amgZoqKMye3LgGeso0EgLv2Ljqh=' : ["pelle", 1 ,1, 1 , 0],
			'fmgZoqKMye3LgGeso0EgLv2Ljqh=' : ["kelle", 0 ,0, 0 , 1],
		}

		return [Host,Port,User,Password,VirtualServer,Queryname,ClientRequiredTs3,ClientRequiredTs3_Warnings,ClientRequiredTs3_KickMessage,ClientRequiredTs3_WarningMessage,ClientRequiredTs3_Channel,Triggerword,Admins]
		

	#elif config_name == SERVER2: 	# or use if config_name == SERVERS[1]
	#	Host 								= "127.0.0.1"
	#	Port								= 10011
	#	User								= "serveradmin"
	#	Password							= "SLMufyy9"
	#	VirtualServer						= 1
	#	Queryname							= "ServerBot"
	#	ClientRequiredTs3 					= True	
	#	ClientRequiredTs3_Warnings			= 3
	#	ClientRequiredTs3_KickMessage 		= "Why oh why did you not just connect to the Ts3 Server"
	#	ClientRequiredTs3_WarningMessage	= "Please connect to our Ts3 Server to play here"
	#	ClientRequiredTs3_Channel			= ["1", "2"]
	#	Triggerword 						= "!ts"
	#	Admins = {
	#		'OmIZoqKMye9L1GeBo0EULv4LdqY=' : ["nux", 1 ,1, 1 , 1],
	#		'amgZoqKMye3LgGeso0EgLv2Ljqh=' : ["pelle", 1 ,1, 1 , 0],
	#		'HSdjASDw8+2kasaJWLsajjbmmba=' : ["alfred", 1 ,1, 1 , 1],
	#		'jkasdh329Mye3Lkjlsi2gjdsf3h=' : ["jonny", 1 ,1, 1 , 1]
	#	}
	#
	#	return [Host,Port,User,Password,VirtualServer,Queryname,ClientRequiredTs3,ClientRequiredTs3_Warnings,ClientRequiredTs3_KickMessage,ClientRequiredTs3_WarningMessage,ClientRequiredTs3_Channel,Triggerword,Admins]
	
	
	#elif config_name == SERVER3:	# or use if config_name == SERVERS[2]
	#	Host 								= "127.0.0.1	
	#	Port								= 10011
	#	User								= "serveradmin"
	#	Password							= "SLMufyy9"
	#	VirtualServer						= 1
	#	Queryname							= "BotMania"
	#	ClientRequiredTs3 					= False
	#	ClientRequiredTs3_Warnings			= 0
	#	ClientRequiredTs3_KickMessage 		= ""
	#	ClientRequiredTs3_WarningMessage	= ""
	#	ClientRequiredTs3_Channel			= ["0", "0"]
	#	Triggerword 						= "!ts"
	#	Admins = {
	#		'OmIZoqKMye9L1GeBo0EULv4LdqY=' : ["nux", 1 ,1, 1 , 1],
	#		'amgZoqKMye3LgGeso0EgLv2Ljqh=' : ["pelle", 1 ,1, 1 , 0],
	#		'amIZoqKMye9L43js70EULkgslqf=' : ["Hotdog", 1 ,1, 1 , 1],
	#		'3kdj3a904lfggGeso0Ehse2Ljqh=' : ["Nils Pils", 1 ,1, 1 , 0]
	#	}
	#
	#	return [Host,Port,User,Password,VirtualServer,Queryname,ClientRequiredTs3,ClientRequiredTs3_Warnings,ClientRequiredTs3_KickMessage,ClientRequiredTs3_WarningMessage,ClientRequiredTs3_Channel,Triggerword,Admins]		
	
	#elif config_name == SERVER4:
	# ...
	# ...

	
	else: 
		return False