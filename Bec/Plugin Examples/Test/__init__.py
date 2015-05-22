import sys
import time
import random
from twisted.internet import task


from Lib import BecClasses
from Lib import Bec_Console_Colors

# A Test class as an example
class Test(object):
	def __init__(self, instance):
		self.becinstance = instance
		self.counter = 0
		self.cnt = 0
		
		#self.show_single_motd = task.LoopingCall(self.single_motd)
		#self.show_single_motd.start(10, False)

		# Do not make packet send calls that are faster than 15ms
		# note: big/heavy functions should not use this
		self.show_fortune = task.LoopingCall(self.fortune)
		self.show_fortune.start(60, False)
		
		#self.show_mass_motd = task.LoopingCall(self.mass_motd)
		#self.show_mass_motd.start(10,False)		

		# Create a looping call for printing time to users ingame. interval at 30 sec on each call.
		self.printTimeTask = task.LoopingCall(self.printTime)
		self.printTimeTask.start(45, False)

	def printTime(self):
		''' Print the current server time to players ingame'''
		rcon_msg = "say -1 "+BecClasses.Timec().GetTime()+" Is the current time on this server"
		self.send(rcon_msg)
	
	def fortune(self):
		''' Show a random fortune. '''

		if self.cnt < 15:
			self.cnt += 1
			
			fortune = ['The force is stonge with you', 'Dont walk the dark path', 'Live long and prosper', 'Share your Happiness with other people']
			indx = random.randrange(0,len(fortune))
			text = "say -1 "+fortune[indx]
			self.send(text)			
		else:
			print "Stopping fortune"
			self.show_fortune.stop()

	def single_motd(self):
		''' An example on how to create a looping call task to show motds ingame '''
		
		# Create a list of strings for our motd messages. "Message of the day"
		smotds = ["Welcome to our fancy server","Enjoy your stay at out server","Hackers caught will get perm banned","No Teamkilling allowed","Lame joiners will get kicked"]			
		smotds_len = len(smotds)-1		
		
		rcon_msg = "say -1 "+smotds[self.counter]		
		self.send(rcon_msg)
		
		if self.counter >= smotds_len: self.counter = 0 
		else: self.counter += 1
		
	def	mass_motd(self):
		''' An example on how to create a looping call task to show mass motds ingame '''
		mmotds = ["abc", "123", "xyz", "789", "AlphaOmega"]
		for msg in mmotds:
			rcon_msg = "say -1 "+msg
			self.send(rcon_msg)
	
	def send(self,data):
		''' Append a rcon command to the queuelist to be sent '''
		self.becinstance._Bec_queuelist.append(data)
		
def start(i):
	Test(i)