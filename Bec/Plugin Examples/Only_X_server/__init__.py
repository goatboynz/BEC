from Lib.BecClasses import Timec


#
# One problems with plugins are that, example: you might run 4 servers. but do not want all of the Bec instances to start up a plugin. you might only want it for server 4.
# To only start up a plugin on a spesific Bec instance/Server we will use Bec's config file name as a referance.
#
# We will add a variable called SERVERS to the __init__.py file. This variable can not be inside a class or a function. it should be in top if the file. like in this example
#
# If the variable is empty like  : SERVERS = [] or SERVERS = () , or if it Does not exsist in the __init__.py file, then Bec will assume all Bec's instances will use the plugin!
# The SERVERS variable needs to be of type LIST or TUPLE
#


#SERVERS = ["a3.cfg", "foo.cfg", "bar.cfg"]
#SERVERS = ("a3.cfg", "foo.cfg", "bar.cfg")  # note. if there is only one element in the TUPLE you need to append a , at the end. SERVERS = ("a3.cfg",) # Basic Python stuff.

SERVERS = ("a3.cfg",)

class My_Plugin(object):
	
	def __init__(self, instance):
		self.bec = instance
		self.Bec_ConfigFile =  self.bec.cfgval.options.filename

	def show_cfgname(self):
		msg = Timec().GetTime()+' : This Bec instance is using config file : '+ self.Bec_ConfigFile
		print msg

def start(i):
	bec = i
	myplugin = My_Plugin(bec)
	myplugin.show_cfgname()

	