

This is a Simple Guid on how to create Python plugins for Bec.
Bec itself is written in Python 2.6. this means we can code plugins written in python.
Using Python 3.x will be considered when some libs such as Twisted will have fully py3 support.

Bec does not come with full python libary's, "Only Some Batteries Included"

If you need to use some 3rd Lib's/Modules for your plugin that is not included in Bec,
then you should use the tool PackLib.exe to extract Bec.lib and add in your 3rd party modules. then repack it again.


* All modules/plugins that is to be started by Bec need to have a ( start ) function with the refrance to the Bec instance (self) as input to the __init__ "constructor" argument.
* All modules/plugins are started as a seperate thread. consider things not to be thread safe!!!
Modules need to be directory's inside the Plugin dir. where the directory is the name of your plugin.


###################################################################################################
A plugin example layout:

Bec\Plugins\MyPlugin

Content Of MyPlugin
:
:
	MyPlugin (Dir)
		|
		|
		__init__.py (File)
		...
		...

Content of __init__.py 
:
: 

-----------------------------------------------------
from twisted.internet import task
class MyPlugin(object):
	''' My Plugin Example '''
	def __init__(self, instance):
		self.bec = instance
		
		self.counter = 0

		''' Create a Task that calls the function Send_HelloWorld each 10th sec. '''
		self.HelloWorld_Task = task.LoopingCall(self.Send_HelloWorld)
		self.HelloWorld_Task.start(10, False)		
	
	def Send_HelloWorld(self):
		'''This Function will send a Global Hello World Message to All Players Ingame.'''
		rcon_msg = "Say -1 Hello World"
		self.bec._Bec_queuelist.append(rcon_msg)
		
		if self.counter < 100:
			self.counter += 1
		else:
			# enough Hello World, Stopping the task
			self.HelloWorld_Task.stop()
		
def start(x):
	pluginObj = Myplugin(x)
	or
	Myplugin(x)





lets start at the bottom.	
the start function takes the instance of bec as the input. and passes this to our MyPlugin class.
This class takes the instance of bec as a input on the __init__ ""constructor"".
this allows us to use functions and variables from bec itself.


###################################################################################################		
Example howto get a list of connected players in your plugin you can do this,

-----------------------------------------------------		
class MyPlugin(object):
	''' My Plugin Example '''
	def __init__(self, instance):
		self.bec = instance
		
		#print get_players()
		#or 
		#print self.bec._Bec_playersconnected
		
	def get_players(self):
		return self.bec._Bec_playersconnected
		


_Bec_playersconnected is a dict where the key is the players guid.
dict = {guid1 : [beid, nick, port, join date], guid2 : [beid, nick, ip, join date] }


###################################################################################################
Another Example that requires sys.path to be used.


Bec\Plugins\MyPlugin

Content Of MyPlugin
:
	MyPlugin (Dir)
		|
		|
		__init__.py (File)
		MyMod.py	(File)

-----------------------------------------------------
:-- __init__.py --:

import sys
import os

# MyMod is a file in the same directory as __init__.py

sys.path.append(os.getcwd()+"\\Plugins\\MyPlugin")
import MyMod 

class Something(object):
	def __init__(self, instance):
		'''blah blah blah'''
		testObj = MyMod()


you should use [ sys.path.append(os.getcwd()+"\\Plugins\\XXX") ] before the import if you need to import modules from the same dir as the __init__ file



-----------------------------------------------------

Q: how can i send a message to a player ?

A: this can be divided in to two questions. how to get a players id and how to send a rcon message.
   to send a message you normaly use the Instance._Bec_queuelist.append(Rcon_cmd)
   but before you can send a rcon message you need to get the id of a player.
   this can be done by checking the Instance._Bec_playersconnected dict, loop over the keys to find the id/name.
   some examples
   
   # ex1
   name = "abc"
   beid = -1
   for key in Instance._Bec_playersconnected.keys():
	if Instance._Bec_playersconnected[key][1] == name:
		beid = Instance._Bec_playersconnected[key][0]
		break
	
	# Or ex2
	guid = abcdef
	beid = -1
	for key in Instance._Bec_playersconnected.keys():
		if key == guid:
			beid = Instance._Bec_playersconnected[key][0]
			break
	
	# Or ex3
	guid = abcdef
	beid = -1
	if Instance._Bec_playersconnected.has_key(guid):
		beid = Instance._Bec_playersconnected[guid][0]

		
	# So now to the send part. thats rather simple. all you have to do is append the command you want to send to Bec's queue list.
	cmd = "say "+str(beid)+" Some message"
	Instance._Bec_queuelist.append(Rcon_cmd)


-----------------------------------------------------
Q: How can i make a plugin only start on only selected Becs' i do not want all Bec's to start a plugin

A: In your Plugin __init__.py file put a variable called SERVER = ["Config.cfg]
   example:
   
   # my __init__.py

   
   SERVERS = ["Server1.cfg" , "Server2.cfg"]

   class MyPlugin(object):
     def __init__(self, instance):
	   self.bec = instance
	   ...
	   ...
	
	This will make Bec start the Plugin for Server 1 and 2. but not any other servers.
	Look at the example provided. Only_X_Server
	
	If you need to have different configuration on your Plugin. one setting for each Bec instance
	Take a look at the TS3 Plugin. Ts3Settings and __init__ files
	
	
	
	
-------------
# Other Questions.	
-------------
Q: I see a bunch of duplicated file names in my plugin directory. example __init__.py , __init__.pyc, __init__.pyo , What are they?.

A: In short. *.py files are source code files.  *.pyc, *.pyo are compiled python files. you can delete the *.pyc and *.pyo files. " IF YOU HAVE THE *.py File"
   So. example. if you have  Whatever.py , Whatever.pyc and or Whatever.pyo you can delete the *.pyc/*.pyo file. 
   If you don't see that the name of the *.pyc / *.pyo files as a *.py file aswell. then don't delete it.
   a side note. if the plugin directory does have *.py files. it will autogenerate *.pyo files from the *.py file.
   Best Advice. Leave the files alone. ;)
   
-------------
Q: I Want to make/release a plugin, but dont want everybody to see my 'ugly' code, Do i need to have *.py files in my plugin directory?.

A: No. *.py files are not needed. Bec will use *.pyc or *.pyo files aswell as *.py.
   But let it be said that, masking your coding in compiled python files is not a good idea. there are ways to get the code.

-------------
Q: How do i make *.pyo files.

A: This is not really a question related to how to make plugins for Bec. If your really intrested in coding plugins, you should look up the python doc.
   After your done with your *.py files for your plugin. run Bec once with the plugin enabled. you should then see it has generated *.pyo files.
   "Stop Bec." Delete all *.py files from your plugin directory. That all.
	
	
For more examples. check the Examples dir

