# -*- encoding: utf-8 -*-


#============================================================
# Status plugin for Arma3 servers.
# This plugin will create a xml file containg info from both Gamespy and Battleye.
# It also have the option to uploade the xml by ftp to a remote host. Ie. your homepage for showoff or whatever...


#============================================================
__version__ 		= "0.11"
__license__ 		= "Gpl v2"
__copyright__ 		= "Copyright 2013, Stian Mikalsen"
__author__ 			= "Stian Mikalsen"
__description__ 	= 'Simple stat generator for Bec'
__author_email__	= "stianmikalsen@hotmail.com"
__maintainer__ 		= "You and yourself. ;)"
#============================================================

import sys
import os
import thread
import time
import datetime
from datetime import timedelta
import random
import struct
import re
import psutil
import codecs
import ftplib
from twisted.internet import task
from twisted.internet import reactor

sys.path.append(os.getcwd()+"\\Plugins\\Status")
import Status_Settings
from Lib.BecClasses import Timec as CT


#-------------------------------------------------------------------------------------------------
# You do not need to edit anything below this line unless you plan on changing/improving the plugin.
SERVERS = Status_Settings.SERVERS


debug = False
class GameSpy(object):
	'''
		This is a simple gamespy query.. its as simple as it gets.
		Only selective data is colleted and does not take multi packets into account.
		It will only collect Server info. not player related data.
	'''
	def __init__(self, instance):
		self.bec = instance
		self.org_func_datagramReceived	= self.bec.datagramReceived
		self.bec.datagramReceived 		= self.datagramReceived
		
		self.base_packet 		= "fefd00"
		self.challenge_packet 	= "fefd09"
		self.id 				= "aaaaaaaa"
		self.info_packet 		= "ffffff01"
		self.serveinfo = {
			"gamever" 		: "N/A", 
			"hostname" 		: "N/A", 
			"mapname" 		: "N/A", 
			"mission" 		: "N/A", 
			"maxplayers" 	: "N/A", 
			'difficulty' 	: "N/A",
			"mod" 			: "N/A",
			"gameState" 	: "N/A",
			"gametype" 		: "N/A", 
			"gamemode" 		: "N/A",
			"password"		: "N/A",
			"equalModRequired" : "N/A",
			"verifySignatures" : "N/A",
			"requiredVersion" : "N/A",
			"reqSecureId"	  : "N/A"
			}
	
	def udp_received(func):
		''' Extend the orginal datagramReceived function.. '''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				# prosess the data comming to bec
				self = args[0]
				pack = args[1]
				hp = pack.encode("hex")
		
				# Response from challenge 2
				if hp[0:10] == "00"+self.id:
					if debug:
						print "res pack 2", args[1].encode("hex"),"\n"
						#print args[1][16::].split("\x01",1)[0],"\n"
						#print args[1][16::].split("\x01",1)[1],"\n"
						#print str(args[1]),"\n"
					
					# split up this crap so we can get the server info we want...
					data = args[1][16::].split("\x01",1)[0].split("\x00")

					# store the gs info into this dict 
					if len(data) > 0:
						try:
							self.serveinfo = {
								"gamever"			: data[data.index("gamever")+1], 
								"hostname"			: data[data.index("hostname")+1], 
								"mapname"			: data[data.index("mapname")+1], 
								"mission"			: data[data.index("mission")+1], 
								"maxplayers"		: data[data.index("maxplayers")+1], 
								"difficulty"		: data[data.index("difficulty")+1], 
								"mod"				: data[data.index("mod")+1], 
								"gameState"			: data[data.index("gameState")+1], 
								"gametype"			: data[data.index("gametype")+1], 
								"gamemode"			: data[data.index("gamemode")+1],
								"password"			: data[data.index("password")+1],
								"equalModRequired"	: data[data.index("equalModRequired")+1],
								"verifySignatures"	: data[data.index("verifySignatures")+1],
								"requiredVersion"	: data[data.index("requiredVersion")+1],
								"reqSecureId"		: data[data.index("reqSecureId")+1]
								}
						except:
							if debug:
								print "error storing gs data to dict"
							pass
						
				# Response to challenge 1
				elif hp[0:10] == "09"+self.id:
					self.gs_challange2(hp)
					if debug:
						print "res pack 1", hp
		return extended_data		
	
	def udp_send(self, data):
		''' Send the data. this will use already exsisting socket that was created when connected. '''
		self.bec.transport.write(data)

	def rnd_hex(self, size):
		
		list = "abcdef0123456789"
		lsize = len(list)-1
		rnr = ""
		while len(rnr) != size:
			rnd = random.randint(0,lsize)
			rnr = rnr + list[rnd]
		return rnr		
	
	def gsquery(self):
		'''Create new id for each challenge that is sent'''
		self.id  = self.rnd_hex(8)
		self.gs_challange1()
	
	def gs_challange1(self):
		'''send gamespy challenge packet 1'''
		pack = self.challenge_packet + self.id
		self.udp_send(pack.decode("hex"))
		if debug:
			print "snd pack 1", pack
	
	def gs_challange2(self, data):
		'''send gamespy challenge packet 2'''
		nd = struct.pack('>i', int(data[10:-2].decode("hex")))
		pack = self.base_packet + self.id + nd.encode("hex") + self.info_packet
		self.udp_send(pack.decode("hex"))
		if debug:
			print "snd pack 2", pack

	#============================================================
	# Decorator...
	@udp_received
	def datagramReceived(self, data, (Bec_Cfg_Main_Host, Bec_Cfg_Main_Port)):
		self.org_func_datagramReceived(data, (Bec_Cfg_Main_Host, Bec_Cfg_Main_Port))

class BecSessionStatus(object):
	
	def __init__(self, instance):
		self.bec = instance
		self.cfgname = self.bec.cfgval.options.filename

		self.settings = Status_Settings.Servers(self.cfgname)
		if self.settings:

			# format for time.
			self.tf = '%H:%M:%S - %Y/%m/%d'
			
			# Set time when this plugin was loaded. "good enough for Bec start time." 
			self.start_time = datetime.datetime.now().strftime(self.tf)
			
			# Get time when the Arma server was started.
			self.arma_starttime = self.get_arma_info()
			if self.arma_starttime == None:
				self.arma_starttime = "N/A"

			self.kts = 0			# Number of kicks this session
			self.bts = 0			# Number of bans this session
			self.hts = 0			# Number of hacks this session		
			self.cts = 0			# Number of connetions this section
			self.unique_guids = []	# list of unique guid that  connected this bec session.
			self.uts = 0			# len of self.unique_guids. 
			
			self.Use_Ftp		= self.settings[0] # Enable ftp or not
			self.Interval		= self.settings[1]
			self.Ftp_Host		= self.settings[2] # ftp add
			self.Ftp_Port		= self.settings[3] # ftp port
			self.Ftp_User		= self.settings[4] # ftp user
			self.Ftp_Password	= self.settings[5] # ftp passw
			self.Ftp_Dir		= self.settings[6] # ftp uploade dir. starts with /dirname or is set to None
			
			#--------------------------------------
			## Make copy fnc.
			self.org_func_be_kick 		= self.bec._be_kick
			self.org_func_be_ban 		= self.bec._be_ban
			self.org_func_be_hack 		= self.bec._be_hack
			self.org_func_connected 	= self.bec._be_connected 
			self.org_func_unverified	= self.bec._be_unverified	
			#self.org_func_verified		= self.bec._be_verified					
				
			## Extend fnc.
			self.bec._be_kick 			= self.player_kick
			self.bec._be_ban 			= self.player_ban
			self.bec._be_hack 			= self.player_hack
			self.bec._be_connected 		= self.connected
			self.bec._be_unverified 	= self.unverified
			#self.bec._be_verified		= self.verified			
			#--------------------------------------
			
			# Table of chars that will be replaced. this is to avoid issues with xml.
			self.html_escape_table = {
				"&" : "&amp;", 
				'"' : "&quot;", 
				"'" : "&apos;",
				">" : "&gt;", 
				"<" : "&lt;",
				"¬" : "&not;",
				"­" : "&shy;",
				"®" : "&reg;",
				"¯" : "&macr;",
				"°" : "&deg;",
				"±" : "&plusmn;",
				"²" : "&sup2;",
				"³" : "&sup3;",
				"´" : "&acute;",
				"µ" : "&micro;",
				"¶" : "&para;",
				"·" : "&middot;",
				"¸" : "&cedil;",
				"¹" : "&sup1;",
				"º" : "&ordm;",
				"»" : "&raquo;",
				"¼" : "&frac14;",
				"½" : "&frac12;",
				"¾" : "&frac34;",
				"¿" : "&iquest;",
				"À" : "&Agrave;",
				"Á" : "&Aacute;",
				"Â" : "&Acirc;",
				"Ã" : "&Atilde;",
				"Ä" : "&Auml;",
				"Å" : "&Aring;",
				"Æ" : "&AElig;",
				"Ç" : "&Ccedil;",
				"È" : "&Egrave;",
				"É" : "&Eacute;",
				"Ê" : "&Ecirc;",
				"Ë" : "&Euml;",
				"Ì" : "&Igrave;",
				"Í" : "&Iacute;",
				"Î" : "&Icirc;",
				"Ï" : "&Iuml;",
				"Ð" : "&ETH;",
				"Ñ" : "&Ntilde;",
				"Ò" : "&Ograve;",
				"Ó" : "&Oacute;",
				"Ô" : "&Ocirc;",
				"Õ" : "&Otilde;",
				"Ö" : "&Ouml;",
				"×" : "&times;",
				"Ø" : "&Oslash;",
				"Ù" : "&Ugrave;",
				"Ú" : "&Uacute;",
				"Û" : "&Ucirc;",
				"Ü" : "&Uuml;",
				"Ý" : "&Yacute;",
				"Þ" : "&THORN;",
				"ß" : "&szlig;",
				"à" : "&agrave;",
				"á" : "&aacute;",
				"â" : "&acirc;",
				"ã" : "&atilde;",
				"ä" : "&auml;",
				"å" : "&aring;",
				"æ" : "&aelig;",
				"ç" : "&ccedil;",
				"è" : "&egrave;",
				"é" : "&eacute;",
				"ê" : "&ecirc;",
				"ë" : "&euml;",
				"ì" : "&igrave;",
				"í" : "&iacute;",
				"î" : "&icirc;",
				"ï" : "&iuml;",
				"ð" : "&eth;",
				"ñ" : "&ntilde;",
				"ò" : "&ograve;",
				"ó" : "&oacute;",
				"ô" : "&ocirc;",
				"õ" : "&otilde;",
				"ö" : "&ouml;",
				"÷" : "&divide;",
				"ø" : "&oslash;",
				"ù" : "&ugrave;",
				"ú" : "&uacute;",
				"û" : "&ucirc;",
				"ü" : "&uuml;",
				"ý" : "&yacute;",
				"þ" : "&thorn;",
				"¡" : "&iexcl;",
				"¢" : "&cent;",
				"£" : "&pound;",
				"¤" : "&curren;",
				"¥" : "&yen;",
				"¦" : "&brvbar;",
				"§" : "&sect;",
				"¨" : "&uml;",
				"©" : "&copy;",
				"ª" : "&ordf;",
				"€" : "&euro;"
				}
			
			# create a instance of out gs class.
			self.gsquery = GameSpy(instance)
			
			# create a task for the gamespy querying.
			self.GsCollect = task.LoopingCall(self.gsquery.gsquery)
			
			# set the query interval for 10 sec between each request.
			self.GsCollect.start(10, False)

			# Start a seperate theread for creating the xml file (and ftp uploade if set to use it)
			thread.start_new_thread(self.create_xmlfile,())
	
	def html_escape(self, text):
		return "".join(self.html_escape_table.get(c,c) for c in text)
	
	def create_xmlfile(self):
		'''create xml file every N sec, interval spesified in the settings file. '''
		while True:
			# aprox sleep
			time.sleep(self.Interval)
		
			#============================================================
			# Create xml string.
			xml_content = False
			try:
				# Set new update time.
				lastupdate_time = datetime.datetime.now().strftime(self.tf)
				nextupdate_time = (datetime.datetime.now() + timedelta(seconds = self.Interval)).strftime(self.tf)	
				
				# Get uptime for the ArmA server.
				aupt = self.get_arma_uptime()
					
				# Get Bec uptime. 
				currenttime = datetime.datetime.now().strftime(self.tf)
				bec_session_time = datetime.datetime.strptime(currenttime, self.tf) - datetime.datetime.strptime(self.start_time, self.tf)	
					
				# Get number of players online, We use battleye here instead of gamespy info about players..
				numplayers = len(self.bec.Bec_playersconnected)
				
				xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'
				xml = xml + '<?xml-stylesheet href="reports.xsl" type="text/xsl" ?>\n'
				xml = xml + '<BecStatus>\n'
				xml = xml + '\t<hostname>'+ self.html_escape(self.gsquery.serveinfo['hostname']) + '</hostname>\n'
				xml = xml + '\t<gamever>'+ self.gsquery.serveinfo['gamever'] + '</gamever>\n'
				xml = xml + '\t<mapname>'+ self.html_escape(self.gsquery.serveinfo['mapname']) + '</mapname>\n'
				xml = xml + '\t<mission>'+ self.html_escape(self.gsquery.serveinfo['mission']) + '</mission>\n'
				xml = xml + '\t<difficulty>'+ self.gsquery.serveinfo['difficulty'] + '</difficulty>\n'
				xml = xml + '\t<numplayers>'+ str(numplayers) + '/' +self.gsquery.serveinfo['maxplayers'] + '</numplayers>\n'
				xml = xml + '\t<lastupdate>'+ str(lastupdate_time) + '</lastupdate>\n'
				xml = xml + '\t<nextupdate>'+ str(nextupdate_time) + '</nextupdate>\n'
				xml = xml + '\t<becversion>'+ self.bec.becversion + '</becversion>\n'
				xml = xml + '\t<beversion>'+ self.bec.beversion + '</beversion>\n'
				xml = xml + '\t<becuptime>'+ str(bec_session_time) + '</becuptime>\n'
				xml = xml + '\t<becreporter>'+ str(self.bec.reporteraccount) + '</becreporter>\n'
				xml = xml + '\t<serveruptime>'+ str(aupt) + '</serveruptime>\n'
				xml = xml + '\t<kts>'+ str(self.kts) + '</kts>\n'
				xml = xml + '\t<bts>'+ str(self.bts) + '</bts>\n'
				xml = xml + '\t<hts>'+ str(self.hts) + '</hts>\n'		
				xml = xml + '\t<cts>'+ str(self.cts) + '</cts>\n'		
				xml = xml + '\t<uts>'+ str(self.uts) + '</uts>\n'
				xml = xml + '\t<numadmins>'+ str(len(self.bec.Bec_adminsconnected)) + '</numadmins>\n'
				xml = xml + '\t<numtmpadmins>'+ str(len(self.bec.Bec_tempadminsconnected)) + '</numtmpadmins>\n'
				xml = xml + '\t<gametype>'+ self.gsquery.serveinfo['gametype'] + '</gametype>\n'			
				xml = xml + '\t<gamemode>'+ self.gsquery.serveinfo['gamemode'] + '</gamemode>\n'
				xml = xml + '\t<gameState>'+ self.gsquery.serveinfo['gameState']+ '</gameState>\n'
				xml = xml + '\t<mod>'+ self.html_escape(self.gsquery.serveinfo['mod'])+ '</mod>\n'
				xml = xml + '\t<password>'+ self.gsquery.serveinfo['password'] + '</password>\n'
				xml = xml + '\t<equalModRequired>'+ self.gsquery.serveinfo['equalModRequired'] + '</equalModRequired>\n'
				xml = xml + '\t<verifySignatures>'+ self.gsquery.serveinfo['verifySignatures'] + '</verifySignatures>\n'
				xml = xml + '\t<requiredVersion>'+ self.gsquery.serveinfo['requiredVersion'] + '</requiredVersion>\n'
				xml = xml + '\t<reqSecureId>'+ self.gsquery.serveinfo['reqSecureId'] + '</reqSecureId>\n'

				xml = xml + '\t<players>\n'		
				# populate the players node if we got players online...
				if numplayers > 0:
					
					for guid in self.bec.Bec_playersconnected.keys():
						ptag = []
						nick = self.bec.Bec_playersconnected[guid][1]
						bid = self.bec.Bec_playersconnected[guid][0]
						lobby = self.bec.Bec_playersconnected[guid][4]

						admin 	= "0" # 0 = none, 1 = admin, 2 = tmp admin
						wrn 	= "0" # warnings given to player
						chatwrn = "0" # chat warnings given to player

					
						# if players is admin or tmp admin.
						if self.bec.Bec_adminsconnected.has_key(nick):
							admin = "1"
						elif self.bec.Bec_tempadminsconnected.has_key(nick):
							admin = "2"
						

						# number of warnings given to the player
						if self.bec.Bec_player_warnings.has_key(nick):
							if self.bec.Bec_player_warnings[nick] > 0:
								wrn = str(self.bec.Bec_player_warnings[nick])
						
						# total chat warnings given to player, sums up from all channels.
						if self.bec.Bec_player_chat_warning.has_key(nick):
							sum = 0
							for e in self.bec.Bec_player_chat_warning[nick]:
								sum = sum + e
							if sum > 0:
								chatwrn = str(sum)
						

						cpy_nick = ""
						try:
							cpy_nick = nick.decode("ascii")
						except:
							try:
								cpy_nick = nick.decode("utf-8")
							except Exception, enc_error1:
								cpy_nick = "N/A"
								if debug:
									print CT().GetTime()+' : Status Plugin, ', enc_error1
								pass
								
						xml = xml + '\t\t<player guid="'+ guid +'" bid="'+ bid +'" wrn="'+wrn+'" chatwrn="'+chatwrn+'" ingame="'+str(lobby)+'" admin="'+admin+'">'+ self.html_escape(cpy_nick) + '</player>\n'

				xml = xml + u'\t</players>\n</BecStatus>\n'
				xml_content = True
			except Exception, err1:
				Logstring = CT().GetTime()+" : Status Plugin, Error in creating xml string"
				self.bec.colorprint.system
				if debug:
					print CT().GetTime()+' :', err1
				pass
			
			#============================================================
			# Write the content to the xml file!..
			xml_created = False
			try:
				if xml_content:
					filepath = 'Plugins\\Status\\Report\\Bec_' + self.bec.Bec_Cfg_Main_LogDirName + '.xml'
					file = codecs.open(filepath, u'wb', encoding='utf-8-sig',errors='ignore')
					file.write(xml)
					file.close()
					xml_created = True
			except Exception, err2:
				Logstring = CT().GetTime()+" : Status Plugin, Error in writing to status.xml file"
				self.bec.colorprint.system(Logstring)
				
				if debug:
					print CT().GetTime()+' :', err2
				pass

			#============================================================
			# Uploade the xml file
			if self.Use_Ftp and xml_created:
				thread.start_new_thread(self.upload,(self.Ftp_Host, self.Ftp_Port, self.Ftp_User, self.Ftp_Password, self.Ftp_Dir, filepath))

	def get_arma_info(self):
		'''Return the time when the server was started. if not possible, return False. '''
		if self.bec.armapid:
			try:
				proc = psutil.Process(self.bec.armapid)
				arma_time = proc.create_time
			except Exception, error:
				arma_time = None
				
				if debug:
					print CT().GetTime()+' : Status Plugin, Error :',error
				pass
			finally:
				return arma_time
		else:
			return None
	
	def get_arma_uptime(self):
		'''
			Calulate the amount of time the serverhas been up.
			This will return N/A if the switch --dsc is used with bec.
		'''
		
		if self.arma_starttime != "N/A":
			a2_time = self.arma_starttime
			a2_starttime = time.strftime(self.tf, time.localtime(a2_time))
			currenttime = datetime.datetime.now().strftime(self.tf)
			tdelta = datetime.datetime.strptime(currenttime, self.tf) - datetime.datetime.strptime(a2_starttime, self.tf)
			return tdelta
		else:
			return "N/A"
	
	def upload(self, ftpadd, ftpprt, ftpuser, ftppw, dir,  file):
		''' will uploade the file to a ftp server.. this function is called from create_xmlfile once the xml file is created.'''
		retrys = 0
		while retrys < 3:
			try:
				ftpclient = ftplib.FTP()
				ftpclient.connect(ftpadd, ftpprt)
				ftpclient.login(ftpuser, ftppw)

				# if using home dir. change the location.
				if self.Ftp_Dir:
					ftpclient.cwd(dir)
					ftp_cmd = 'STOR '+dir+'/'+file.split("\\")[-1]
				else:
					ftp_cmd = 'STOR '+file.split("\\")[-1]
				
				xmlfile = open(os.getcwd()+"\\"+file ,'rb')
				ftpclient.storbinary(ftp_cmd , xmlfile)
		
				xmlfile.close()
				ftpclient.quit()
				
				retrys = 3
				break
			except Exception, error:
				print CT().GetTime()+' : Status Plugin, Ftp Error :',error
				retrys += 1
				
				if debug:
					print CT().GetTime()+' :', error
				pass

	#============================================================
	# functions that will hook into the orginale functions and add extra data. so called monkey patching...
	def Be_PlayerConnected(func):
		''' A player connected to the server. increase the counter by +1 '''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self = args[0]
				self.cts +=1
		return extended_data	
	def Be_PlayerUnverified(func):
		'''
			Check if the connected player_guid is in our list of guids.
			if not so, increase the unique players guid list conter by +1.
			this is a overall couner of unique players connected to the server in this bec session.
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self = args[0]
				vdata = args[1].groups()
				guid = vdata[0]
				if not guid in self.unique_guids:
					self.uts += 1
					self.unique_guids.append(guid)
					

		return extended_data		
	def Be_PlayerKick(func):
		'''when a kick happens. increase the kick counter by +1.'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self = args[0]
				self.kts += 1
		return extended_data
	def Be_PlayerBan(func):
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self = args[0]
				self.bts += 1
		return extended_data			
	def Be_PlayerHack(func):
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self = args[0]
				self.hts += 1
		return extended_data			
	
	#============================================================
	# Deorators
	@Be_PlayerConnected
	def connected(self, data):
		self.org_func_connected(data)		
	@Be_PlayerKick
	def player_kick(self, a1, a2, a3, a4, a5):
		self.org_func_be_kick(a1, a2, a3, a4, a5)
	@Be_PlayerBan
	def player_ban(self, a1, a2, a3, a4, a5):
		self.org_func_be_ban(a1, a2, a3, a4, a5)
	@Be_PlayerHack
	def player_hack(self, a1, a2, a3, a4, a5):
		self.org_func_be_hack(a1, a2, a3, a4, a5)
	@Be_PlayerUnverified
	def unverified(self, data):
		self.org_func_unverified(data)	

def start(x):
	status = BecSessionStatus(x)
