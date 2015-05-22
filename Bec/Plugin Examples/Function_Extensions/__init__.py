
class Function_Extensions(object):
	'''A Example Class to Extend some functions in Bec'''
	def __init__(self, instance):
		self.bec = instance
		self.mytext = "This is just an example text string!"

		########################################################
		## Orginale functions we want to extend. Make a copy. ##
		
		# the function that triggers when a player connects.
		self.org_func_connected 	= self.bec._be_connected 	
		
		# the function that triggers when a player disconnects.
		self.org_func_disconnected 	= self.bec._be_disconnected	
		
		# the function that triggers when a player gets unverified.
		self.org_func_unverified	= self.bec._be_unverified	
		
		# the function that triggers when a player gets verified.
		self.org_func_verified		= self.bec._be_verified		
		
		# the function that triggers when a player chats.
		self.org_func_chat			= self.bec._be_chat			

		################################
		## Monkey patch the functions ##
		self.bec._be_connected 		= self.connected
		self.bec._be_disconnected 	= self.disconnected
		self.bec._be_unverified 	= self.unverified
		self.bec._be_verified		= self.verified
		self.bec._be_chat 			= self.chat

	def Be_PlayerConnected(func):
		'''
			This will extend the connected function.
			Add your extra code into extended_data -> finally.
		
			Arg 0 can be considered as self.
			Arg 1 will be a regex obj
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
			
				player_name = args[1].groups()[1]
				player_ipp	= args[1].groups()[2].split(":")
				
				player_ip = player_ipp[0]
				player_port = player_ipp[1]
			
				print "name:",player_name," Connected with Ip:",player_ip," Using Port:",player_port
				
				
					
		return extended_data
	def Be_PlayerDisconnected(func):
		'''
			This will extend the disconnected function
			Add your extra code into extended_data -> finally.
		
			arg 0 can be considered as self.
			arg 1 will be a regex obj
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:

				player_name = args[1].groups()[0]
				print player_name,"Has Disconnected from the Server"
				
				
		return extended_data
	def Be_PlayerUnverified(func):
		'''
			This will extend the unverified function
			Add your extra code into extended_data -> finally.
	
			Arg 0 can be considered as self.
			Arg 1 will be a regex obj
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				udata = args[1].groups()
				beid = udata[0]
				nick = udata[1]
				guid = udata[2]
				print "guid "+guid+" of player "+nick+" has been unverified"
		
		return extended_data
	def Be_PlayerVerified(func):
		'''
			This will extend the verified function
			Add your extra code into extended_data -> finally.
		
			Arg 0 can be considered as self.
			Arg 1 will be a regex obj		
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				vdata = args[1].groups()
				guid = vdata[0]
				beid = vdata[1]
				nick = vdata[2]
				
				print "guid "+guid+" of player "+nick+" has been verified"
				
		return extended_data
	def Be_PlayerChat(func):
		'''
			This will extend the connected function
			Add your extra code into extended_data -> finally.
		
			Arg 0 can be considered as self.
			Arg 1 will be a regex obj
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				
				self			= args[0]
				cdata 			= args[1].groups()
				chat_channel 	= cdata[0]
				player_name 	= cdata[1]
				chat_text 		= cdata[2]

				# UNSAFE 
				if player_name == "nux" and chat_text.lower() == "danger":
					print self.mytext
				

				# SAFEST
				if chat_text.lower() == "danger":
					# We dont know the guid, so find the guid assosiated with the player name
					for guid in self.bec._Bec_playersconnected.keys():
						try:
							if self.bec._Bec_playersconnected[guid][1] == player_name:
								print "Got the guid:",guid,"of player:",player_name
								print "You can now make events based on input from this player."
								break
						except:
							print "Some error occured trying to find the player guid"
					else:
						print "No players are yet verified.. can not get the player guid."
				else:
					print "type danger on the chat"

		return extended_data	
	
	# Use decorators to extend the functions
	@Be_PlayerConnected	
	def connected(self,data):
		'''This is a moneky patched function which uses a decorator to extends the orginale function'''
		self.org_func_connected(data)
	
	@Be_PlayerDisconnected
	def disconnected(self,data):
		'''This is a moneky patched function which uses a decorator to extends the orginale function'''
		self.org_func_disconnected(data)
	
	@Be_PlayerUnverified
	def unverified(self,data):
		'''This is a moneky patched function which uses a decorator to extends the orginale function'''
		self.org_func_unverified(data)		
	
	@Be_PlayerVerified
	def verified(self,data):
		'''This is a moneky patched function which uses a decorator to extends the orginale function'''
		self.org_func_verified(data)	
	
	@Be_PlayerChat
	def chat(self,data):
		'''This is a moneky patched function which uses a decorator to extends the orginale function'''
		self.org_func_chat(data)

def start(i):
	Function_Extensions(i)
