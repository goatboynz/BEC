# -*- encoding: utf-8 -*-
__version__ 		= "0.21"
__license__ 		= "Gpl v2"
__copyright__ 		= "Copyright 2013, Stian Mikalsen"
__author__ 			= "Stian Mikalsen"
__description__ 	= 'Ts3 plugin'
__author_email__	= "stianmikalsen@hotmail.com"
__maintainer__ 		= "Stian Mikalsen"

import sys
import os
import time
import telnetlib
import logging
import thread
from threading import Lock
from twisted.internet import task
from Lib.BecClasses import Timec as CT

sys.path.append(os.getcwd()+"\\Plugins\\Ts3")
import Ts3_Settings
from Ts3Classes import *

#-------------------------------------------------------------------------------------------------
# You do not need to edit anything below this line unless you plan on changing/improving the plugin.
SERVERS = Ts3_Settings.SERVERS

debug = False
if debug:
	print CT().GetTime()+' : Ts3 Debug Mode On!!!'

class BecTs3(object):
	'''
		A Ts3 Plugin for Bec.
		This plugin will extend some function in Bec
		Feel Free to modify it..
	'''
	def __init__(self, instance):
		
		self.bec = instance
		self.Bec_ConfigFile =  self.bec.cfgval.options.filename  		# Get the config file the current Bec instance uses.
		self.Ts3Settings = Ts3_Settings.Ts3Servers(self.Bec_ConfigFile)	# Get the settings for this config file.
		
		self.ts3_stack = []
		if self.Ts3Settings:

			self.Collect_Loop_Time = 20 # sec for each time a ts3 query request.	
			
			# settings from the settings.py file
			self.ts3settings = {
				'ts3_host'						: self.Ts3Settings[0], 
				'ts3_port'						: self.Ts3Settings[1],
				'ts3_user'						: self.Ts3Settings[2],
				'ts3_password'					: self.Ts3Settings[3],
				'ts3_vserv' 					: self.Ts3Settings[4],
				'ts3_clientname' 				: self.Ts3Settings[5],
				'ts3_required_connection'		: self.Ts3Settings[6],
				'ts3_required_numwarnings'		: self.Ts3Settings[7],
				'ts3_required_kick_message'		: self.Ts3Settings[8],
				'ts3_required_warn_message'		: self.Ts3Settings[9],
				'ts3_channles'					: self.Ts3Settings[10],
				'ts3_triggerword'				: self.Ts3Settings[11],
				'ts3_admins'					: self.Ts3Settings[12]
			}
			
			
			# This are kick messages we like to ignore. no need to send them to ts3 admins
			# Note. BE kick messages are max 64 chars long, the items in this list will be truncated to 64 chars if they are longer.
			self.BE_msg_ignores = (
				"Client not responding",
				"Invalid GUID",
				"Ping too high (",
				"Unknown Game Version",
				"Corrupted Memory #",
				"Global Ban #",
				"Failed to update",
				"Bad Player Name",
				"Admin Kick (BEC : Invalid Name)",
				"Admin Kick (BEC : Fix your player name, it needs to be ASCII chars only)",
				"Admin Kick (BEC : Lobby idling to long)",
				"Admin Kick (BEC : Only Reserved Slots Left)",
				"Admin Kick (BEC : Your player name is to long)",
				"Admin Kick (BEC : Your guid is not white-listed on this server)",
				"Admin Kick (BEC : Your player name is not allowed on this server)",
				"Admin Kick (BEC : Your player name can not contain any of the chars:",
				"Admin Kick ("+self.bec.Bec_Cfg_Misc_WhileListKickMsg+")",
				"Admin Kick ("+self.bec.Bec_Cfg_Misc_SlotLimit_Msg+")",
				"Admin Kick ("+self.ts3settings['ts3_required_kick_message'],
				"Admin Kick (BEC : This name is not allowed to be used to this server)"
				)
			
		
			# Normaly the trigger word would be enough, but since Bec might have some restrictions on channels,
			# to avoid giving warning, add the triggerword to the commandlist.
			# for the command dict, the 1st item must be 100. the last item is the desctription of the command.
			# all other items in the list is set as a empty string.
			self.bec._Bec_commands[self.ts3settings['ts3_triggerword']] = [100, "", "", "", "Notify a ts3 admin about a problem."]

			self.ts3_channelid_deny 	= []
			self.ts3_channelid_allow 	= []
			self.ts3_player_warning 	= {} 
			self.ts3_clients 			= {}
			self.ts3_server 			= None
			self.ts3_channels 			= False
			self.ts3_connected 			= False
			self.get_clientinfo_ret = 0
			
			## Make copy.
			self.org_func_connected 	= self.bec._be_connected
			self.org_func_disconnected 	= self.bec._be_disconnected
			self.org_func_be_kick 		= self.bec._be_kick
			self.org_func_be_ban 		= self.bec._be_ban
			self.org_func_be_hack 		= self.bec._be_hack
			self.org_func_chat			= self.bec._be_chat
			
			## Extend
			self.bec._be_connected = self.player_connected     
			self.bec._be_disconnected = self.player_disconnected
			self.bec._be_kick = self.player_kick
			self.bec._be_ban = self.player_ban
			self.bec._be_hack = self.player_hack
			self.bec._be_chat = self.player_chat	            
			

			# Start the work threads
			self.Ts3CollectLoopTask = task.LoopingCall(self.Ts3_threadtask)
			#self.Ts3CollectLoopTask.start(self.Collect_Loop_Time, False)
			
			thread.start_new_thread(self.Ts3_msg_stack,())
						
			def admin_settings(admins, type):
				a = {}
				for uid in admins:
					if admins[uid][type] == 1:
						a[uid] = admins[uid]
				return a
			self.adminlist_kick = admin_settings(self.ts3settings['ts3_admins'], 1)
			self.adminlist_ban 	= admin_settings(self.ts3settings['ts3_admins'], 2)
			self.adminlist_hack = admin_settings(self.ts3settings['ts3_admins'], 3)
			self.adminlist_chat = admin_settings(self.ts3settings['ts3_admins'], 4)
			
			# Connect function.
			self.Ts3_connect(
				self.ts3settings['ts3_host'], 
				self.ts3settings['ts3_port'], 
				self.ts3settings['ts3_user'], 
				self.ts3settings['ts3_password'],
				self.ts3settings['ts3_vserv'],
				self.ts3settings['ts3_clientname'],
				self.ts3settings['ts3_channles']
				)
		
		else:
			Logstring =  CT().GetTime()+' : The Ts3 Plugin is not Configured for this server, Recheck settings'
			self.bec.colorprint.system(Logstring)
			if debug:
				print CT().GetTime()+' :',self.Bec_ConfigFile,':',SERVERS
	
	## ----------------------- ##
	# Ts3 functions...
	def Ts3_connect(self, host, port, user, password, vserver, clientname, channels):
		'''
			This funcion does the connect, login etc .. part.
			if it dosent fail, it will start the Ts3_collect_loop function
		'''
		########################################
		# try and connect n times.
		reconnect = 0
		while reconnect < 4:
			reconnect = reconnect + 1
			
			# --------------------------
			# Connect..
			try:
				self.ts3_server = TS3Server(host, port)
				self.ts3_connected = True
				reconnect = 4

				Logstring = CT().GetTime()+' : Ts3 ServerQuery connecting to server : '+str(host)+":"+str(port)
				self.bec.colorprint.default(Logstring)
				break
			except Exception, Ts3_connect_error:
				Logstring = CT().GetTime()+' : Ts3 ServerQuery connection failed, retry ' + str(reconnect) + '/4'
				self.bec.colorprint.system(Logstring)
				pass
					
			time.sleep(4)

		
		########################################
		# if we got connected.
		if self.ts3_connected :
			# --------------------------
			# Log in..
			try:
				self.ts3_server.login(str(user), str(password))
				Logstring = CT().GetTime()+' : Ts3 ServerQuery logged in'
				self.bec.colorprint.default(Logstring)			
			except Exception, Ts3_login_error:
				Logstring = CT().GetTime()+' : Ts3 ServerQuery login failed'
				self.bec.colorprint.system(Logstring)

				
			# --------------------------
			# Set virtual server
			try:
				self.ts3_server.use_vs(vserver)
			except Exception, Ts3_VServer_error:
				Logstring = CT().GetTime()+' : Ts3 ServerQuery virtual server selection failed'
				self.bec.colorprint.system(Logstring)
				self.ts3_connected = False

			# --------------------------
			# Set query client nick name.
			try:
				if self.ts3_connected:
					self.ts3_server.query_name_changer(str(clientname))
			except Exception, Ts3_Clientname_error:
				Logstring = CT().GetTime()+' : Ts3 ServerQuery failed to set client query name'
				self.bec.colorprint.system(Logstring)

								
			# --------------------------
			# Collect all channels so we can get the CID. "Channel Id"
			try:
				if not self.ts3_channels and self.ts3_connected:
					self.ts3_channels = self.ts3_server.channellist()
				
				# if we have set spesific channels.
				if len(channels) >= 1:
						
					# Loop over all cid set to be allowed/dissallowed...
					for cn in channels:
												
						# loop over channels recived from ts3 server
						for tcn in self.ts3_channels:

							# Get black listed channels. backlisted channels starts with !
							if cn.startswith("!") and len(cn) > 1:
								if cn[1::] == tcn['cid']:
									self.ts3_channelid_deny.append(tcn['cid'])
							else:
								if tcn['cid'] == cn:
									self.ts3_channelid_allow.append(tcn['cid'])
												
							# Dont use both types, meaning. cant use allow and disallow at the same time.
							if len(self.ts3_channelid_allow) > 0 and len(self.ts3_channelid_deny) > 0:
								self.ts3_channelid_allow = []
								self.ts3_channelid_deny = []
								Logstring = CT().GetTime()+' : TS3 Config Error : Can not use both allow and deny methode. Allow all channels set'
								self.bec.colorprint.system(Logstring)
			except Exception, Ts3_channellist_error:
				self.ts3_connected = False
				Logstring = CT().GetTime()+' : Ts3 ServerQuery failed to receive the channel list'
				self.bec.colorprint.system(Logstring)

			
			# Start looping task.
			try:
				self.Ts3CollectLoopTask.start(self.Collect_Loop_Time, True)
			except:
				pass

		
		elif not self.ts3_connected and reconnect >= 4:
			try:
				self.Ts3CollectLoopTask.stop()
			except:
				# if the task is not running, it will raise a error if trying to stop something thats not running.
				# safely ignore the error.
				pass
			Logstring = CT().GetTime()+' : Ts3 ServerQuery connection could not be made'
			self.bec.colorprint.system(Logstring)
	
	def Ts3_collect(self):
		'''
			This function will request ts3 user info, connected arma3 players. and do its stuff according to what the settings are like.
			Basic task of this function is to kick or send Arma3 players messages about getting on the Ts3 server
		'''

		def get_clientinfo():
			clients = None
			try:
				clients = self.ts3_server.clientinfo()
				self.get_clientinfo_ret = 0
			except Exception, Ts3_clientinfo_error:
				pass


			if clients:
				return clients
			else:
				# if we could not get the clients retry 3 times before we reconnect.
				self.get_clientinfo_ret += 1

				if self.get_clientinfo_ret >= 3:
					Logstring = CT().GetTime()+' : Ts3 ServerQuery connection has most likely been lost'
					self.bec.colorprint.system(Logstring)
					
					# reinit
					self.ts3_channelid_deny 	= []
					self.ts3_channelid_allow 	= []
					self.ts3_player_warning 	= {} 
					self.ts3_clients 			= {}
					self.ts3_server 			= False
					self.ts3_channels 			= False
					self.ts3_connected 			= False
					# and reconnect !!
					
					#try:
					#	self.Ts3CollectLoopTask.stop()
					#except:
					#	pass
						
					self.Ts3_connect(
						self.ts3settings['ts3_host'], 
						self.ts3settings['ts3_port'], 
						self.ts3settings['ts3_user'], 
						self.ts3settings['ts3_password'],
						self.ts3settings['ts3_vserv'],
						self.ts3settings['ts3_clientname'],
						self.ts3settings['ts3_channles']
						)			
				else:
					get_clientinfo()

		# if we are connected. do some stuff.
		if self.ts3_connected:
			try:
				# if num players is greater than or equal to 0.. 
				if len(self.bec.Bec_playersconnected) >= 0:
					
					# get the client info from the function
					self.ts3_clients = get_clientinfo()

					# Only do this block of code if we have clients on the ts3..
					if self.ts3_clients:
						# Collect all Ip's from Bec and Ts3 server
					
						# Get ts3 clients
						ctdict = {}
						for v in self.ts3_clients.values():
							ip = v[1]
							cid = v[2]
							if ip != None:
								ctdict[ip] = cid
							
						# Get arma/be clients
						for pk in self.bec.Bec_playersconnected.keys():
							
							beid 	= self.bec.Bec_playersconnected[pk][0]
							nick 	= self.bec.Bec_playersconnected[pk][1]
							pip 	= self.bec.Bec_playersconnected[pk][2]
							ingame 	= self.bec.Bec_playersconnected[pk][4]

							# we ignore players who are in the lobby and also admins, so we only send this to normal players who are ingame
							if ingame == 1 and not self.bec._Bec_admins.has_key(pk) and self.ts3settings['ts3_required_connection']:

								# Player Is Missing on Ts3 Check, send warning or kick..
								if not ctdict.has_key(pip):
				
									# if we have enabled warnings show it to the player.
									if self.ts3settings['ts3_required_numwarnings'] > 0:	

										try:
											# increase the warn counter by 1 for the player
											warnings = self.ts3_player_warning[nick]
											warnings += 1
											self.ts3_player_warning[nick] = warnings
										except:
											# if the player has no key set. init one with value of 1
											self.ts3_player_warning[nick] = 1
											warnings = self.ts3_player_warning[nick]
											
										# kick the player
										if warnings > self.ts3settings['ts3_required_numwarnings']:
											cmd = "kick "+beid+" "+self.ts3settings['ts3_required_kick_message']
											self.bec._Bec_queuelist.append(cmd)
											if debug:
												print CT().GetTime()+' :',cmd
										# send warning to the player
										else:
											cmd = "say "+beid+" "+self.ts3settings['ts3_required_warn_message']
											self.bec._Bec_queuelist.append(cmd)
											if debug:
												print CT().GetTime()+' :',cmd
									
									# No warnings.. Instant kick
									elif self.ts3settings['ts3_required_numwarnings'] == 0:
										cmd = "kick "+beid+" "+self.ts3settings['ts3_required_kick_message']
										self.bec._Bec_queuelist.append(cmd)
										if debug:
											print CT().GetTime()+' :',cmd
									else:
										if debug:
											print CT().GetTime()+' : umf wrn not sure why this happend.'
										
								# Player Connected.. but more checks needed.
								elif ctdict.has_key(pip):

									# allow channel ?
									if len(self.ts3_channelid_allow) > 0:
											
										# All is Ok. Player is in correct channel so no need to do more.
										if ctdict[pip] in self.ts3_channelid_allow:
											self.ts3_player_warning[nick] = 0
											
										# Wrong Channel
										else:
											# if we have enabled warnings.
											if self.ts3settings['ts3_required_numwarnings'] > 0:	
												
												try:
													warnings = self.ts3_player_warning[nick]
													warnings += 1
													self.ts3_player_warning[nick] = warnings
												except:
													self.ts3_player_warning[nick] = 1
													warnings = self.ts3_player_warning[nick]

												if warnings > self.ts3settings['ts3_required_numwarnings']:
													cmd = "kick "+beid+" "+self.ts3settings['ts3_required_kick_message']
													self.bec._Bec_queuelist.append(cmd)
													if debug:
														print CT().GetTime()+' :',cmd
												else:
													cmd = "say "+beid+" "+self.ts3settings['ts3_required_warn_message']
													self.bec._Bec_queuelist.append(cmd)
													if debug:
														print CT().GetTime()+' :',cmd
												
											# No warnings.. Instant kick
											elif self.ts3settings['ts3_required_numwarnings'] == 0:
												cmd = "kick "+beid+" "+self.ts3settings['ts3_required_kick_message']
												self.bec_Bec_queuelist.append(cmd)
												if debug:
													print CT().GetTime()+' :',cmd
											else:
												if debug:
													print CT().GetTime()+' : umf cwc not sure why this happend.'
									# deny channel ?
									else:
										# Check if the player is in a denyed channel
										if len(self.ts3_channelid_deny) > 0:
												
											if ctdict[pip] in self.ts3_channelid_deny:
												# if we have enabled warnings.
												if self.ts3settings['ts3_required_numwarnings'] > 0:	
													try:
														warnings = self.ts3_player_warning[nick]
														warnings += 1
														self.ts3_player_warning[nick] = warnings
													except:
														self.ts3_player_warning[nick] = 1
														warnings = self.ts3_player_warning[nick]

													if warnings > self.ts3settings['ts3_required_numwarnings']:
														cmd = "kick "+beid+" "+self.ts3settings['ts3_required_kick_message']
														self.bec._Bec_queuelist.append(cmd)
														if debug:
															print CT().GetTime()+' :',cmd
													else:
														cmd = "say "+beid+" "+self.ts3settings['ts3_required_warn_message']
														self.bec._Bec_queuelist.append(cmd)
														if debug:
															print CT().GetTime()+' :',cmd
												# No warnings.. Instant kick
												elif self.ts3settings['ts3_required_numwarnings'] == 0:
													cmd = "kick "+beid+" "+self.ts3settings['ts3_required_kick_message']
													self.bec._Bec_queuelist.append(cmd)
													if debug:
														print CT().GetTime()+' :',cmd
												else:
													if debug:
														print CT().GetTime()+' : umf cdc not sure why this happend.'
											else:
												# If the player is not in a deny channel. reset the warning counter.
												self.ts3_player_warning[nick] = 0
			except Exception, Ts3_collect_error:
				pass
	
	def Ts3_threadtask(self):
		''' start new work thread to collect ts3 info on socket..'''
		try:
			thread.start_new_thread(self.Ts3_collect,())
		except Exception, Ts3_threadtask_error:
			if debug:
				print CT().GetTime()+' :',Ts3_threadtask_error
			pass
	
	def Ts3_msg_stack(self):
		''' 
			a thread that will work as loop , all messages sendt to admins are handled by this thread.
			messages will be sent with 1.5 sec delay
		    This is done incase multiple things happen, ie chat and kick at same time
			if packets are sendt with little to no delay. they may not be recived by the server.
		'''
		while True:
			time.sleep(1.5)
			try:
				if len(self.ts3_stack)  > 0:
					admins 	= self.ts3_stack[0][0]
					msg 	= self.ts3_stack[0][1]
					self.ts3_server.send_admin_message(admins, msg)
					self.ts3_stack.pop(0)
			except Exception, Ts3_msgstack_error:
				if debug:
					Logstring = CT().GetTime()+' : Ts3 msg stack error'
					self.bec.colorprint.system(Logstring)
				pass

	## ----------------------- ##
	# Extended Bec functions...
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
				'''Create a key using the name and init the value to 0 for each player who connects.'''
				self = args[0]
				player_name = args[1].groups()[1]
				self.ts3_player_warning[player_name] = 0
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
				'''This will just clean up the ts3_player_warning dict so it doesnt just keep growing.'''
				self = args[0]
				name = args[1].groups()[0]
				try:
					del self.ts3_player_warning[name]
				except:
					pass
		return extended_data	
	
	def Be_PlayerKick(func):
		'''
			This function will trigger once a player gets kicked.
			it will notify a ts3 admins who are set to get "nok" messages.
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self	= args[0]

				beid 	= args[1]
				name 	= args[2]
				guid 	= args[3] 
				pip 	= args[4]
				reason 	= args[5]
				
				if self.ts3_connected:

					sendts3msg = True
					for bemsg in self.BE_msg_ignores:
						
						# Reasons on battleye has a max length of 64 chars.. its suppose to increase in future.
						if len(bemsg) > 64:
							bemsg = bemsg[0:64]

						if reason.decode("utf-8").startswith(bemsg):
							sendts3msg = False
							break

					if sendts3msg:

						if len(self.adminlist_kick) > 0:
							msg = name + " : Was Kicked : " + reason
							self.ts3_stack.append([self.adminlist_kick, msg])
							if debug:
								print CT().GetTime()+' :',msg
		return extended_data
	
	def Be_PlayerBan(func):
		'''
			This function will trigger once a player gets banned
			it will notify a ts3 admins who are set to get "nob" messages.
		'''	
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self	= args[0]
				beid 	= args[1]
				name 	= args[2]
				guid 	= args[3] 
				pip 	= args[4]
				reason 	= args[5]
				
				if self.ts3_connected:

					if len(self.adminlist_ban) > 0:
						msg = str(name) + " : Was banned : " + reason
						self.ts3_stack.append([self.adminlist_ban, msg])
						
						if debug:
							print CT().GetTime()+' :',msg
		return extended_data			
	
	def Be_PlayerHack(func):
		'''
			This function will trigger once a player gets caught for gamehack/battleye hack
			it will notify a ts3 admins who are set to get "noh" messages.
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self	= args[0]
				beid 	= args[1]
				name 	= args[2]
				guid 	= args[3] 
				pip 	= args[4]
				reason 	= args[5]
				if self.ts3_connected:

					if len(self.adminlist_hack) > 0:
						msg = str(name) + " : Was Kicked For: " + reason
						self.ts3_stack.append([self.adminlist_hack, msg])
						
						if debug:
							print CT().GetTime()+' :',msg
		return extended_data			
	
	def Be_PlayerChat(func):
		'''
			This function will trigger once a player sends some chat.
			Add your extra code into extended_data -> finally.
		
			Arg 0 can be considered as self.
			Arg 1 will be a regex obj
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				''' it will notify a ts3 admins who are set to get "nfu" messages. '''
				self = args[0]
				chat_channel 	= args[1].groups()[0]
				name 			= args[1].groups()[1]
				chat_text 		= args[1].groups()[2]
				beid = "-1" 	# default, set to all.

				if chat_text.startswith(self.ts3settings['ts3_triggerword']) and self.ts3_connected:
					
					# Get the beid of the player.. players get id once they are unverified/verified
					for guid in self.bec.Bec_playersconnected.keys():
						if self.bec.Bec_playersconnected[guid][1] == name:
							beid = self.bec.Bec_playersconnected[guid][0]
							break

					if len(chat_text) >= len(self.ts3settings['ts3_triggerword']) + 5:
						
						msg = str(name)+" : " + chat_text[4::]
						if len(self.adminlist_chat) > 0:
							self.ts3_stack.append([self.adminlist_chat, msg])
							cmd = "say "+str(beid)+" Your Ts3 message has been sent to the Ts3 Admins. Thank you!"
							self.bec._Bec_queuelist.append(cmd)
							if debug:
								print CT().GetTime()+' :',cmd
					else:
						cmd = "say "+str(beid)+" Your Ts3 message is to short. use atleast 4 letters."
						self.bec._Bec_queuelist.append(cmd)
						if debug:
							print CT().GetTime()+' :',cmd
		return extended_data		
	
	@Be_PlayerConnected
	def player_connected(self, data):
		self.org_func_connected(data)
		
	@Be_PlayerDisconnected
	def player_disconnected(self,data):
		self.org_func_disconnected(data)	
	
	@Be_PlayerKick
	def player_kick(self, a1, a2, a3, a4, a5):
		self.org_func_be_kick(a1, a2, a3, a4, a5)

	@Be_PlayerBan
	def player_ban(self, a1, a2, a3, a4, a5):
		self.org_func_be_ban(a1, a2, a3, a4, a5)
	
	@Be_PlayerHack
	def player_hack(self, a1, a2, a3, a4, a5):
		self.org_func_be_hack(a1, a2, a3, a4, a5)

	@Be_PlayerChat
	def player_chat(self, data):
		self.org_func_chat(data)		

def start(x):
	tsobj = BecTs3(x)

