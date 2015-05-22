

class Function_Replacing(object):
	''' A Example Class to Replace some functions in Bec '''
	def __init__(self, instance):
		self.bec = instance
		
		self.bec._be_connected 		= self.connected
		self.bec._be_disconnected 	= self.disconnected
	
	def connected(self,data):
		'''
			This function will totaly replace Becs connected function.
			!!! WARNING !!! 
			If you dont know what your doing, dont do this!!
		'''
		name = data.groups()[1]
		try:
			print name.decode("utf-8") + " Has joined!"
		except:
			''' chinees mf '''
			print name + " Has joined!"
	
	def disconnected(self,data):
		'''
			This function will totaly replace Becs disconnected function.
			!!! WARNING !!! 
			If you dont know what your doing, dont do this!!
		'''	
		name = data.groups()[0]
		print name + " Has quit!"

def start(i):
	Function_Replacing(i)
