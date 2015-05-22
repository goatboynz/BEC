# -*- encoding: utf-8 -*-

#============================================================
__version__ 		= "0.1"
__license__ 		= "Gpl v2"
__copyright__ 		= "Copyright 2013, Stian Mikalsen"
__author__ 			= "Stian Mikalsen"
__description__ 	= 'Connection limiter for Bec'
__author_email__	= "stianmikalsen@hotmail.com"
__maintainer__ 		= "You and yourself. ;)"
#============================================================

import os
import sys
import time
import datetime
from datetime import timedelta
from twisted.internet import task

sys.path.append(os.getcwd()+"\\Plugins\\\ConnectionLimiter")
import CL_Settings
from Lib.BecClasses import Timec as CT

SERVERS = CL_Settings.SERVERS

class Conlimit(object):

	def __init__(self, instance):
		self.bec = instance
		self.cfgname = self.bec.cfgval.options.filename
		self.settings = CL_Settings.Servers(self.cfgname)
		
		if self.settings:

			self.connections_total	 		= 0	
			self.connections_total_delta	= 0	 		
			self.server_lock_time 			= None
			self.server_locked 				= False
			self.samptime 					= self.settings[0]
			self.locktime 					= self.settings[1]
			self.consec						= self.settings[2]
						
			self.org_func_connected 		= self.bec._be_connected
			self.bec._be_connected 			= self.connected

			self.limiter_task = task.LoopingCall(self.limiter)
			self.limiter_task.start(self.samptime, False)
			
	def limiter(self):
		''' this function is started and run by a looping task'''
		x = self.connections_total - self.connections_total_delta
		if x >= self.consec:
			self.server_locked 		= True
			self.server_lock_time 	= datetime.datetime.now()
			self.bec._Bec_queuelist.append("#lock")
			print CT().GetTime()+" : Bec Activating Flood Control : Server Locked"
		else:
			if self.server_locked:
				checktime = self.server_lock_time + timedelta(seconds=self.locktime)
				if checktime < datetime.datetime.now():
					self.server_locked = False
					self.bec._Bec_queuelist.append("#unlock")
					print CT().GetTime()+" : Bec Deactivating Flood Control : Server Unlocked"

		self.connections_total_delta = self.connections_total
	
	def onConnected(func):
		''' this function is triggered when players connect'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self = args[0]
				self.connections_total +=1
		return extended_data
	
	@onConnected
	def connected(self, data):
		self.org_func_connected(data)		
		
def start(x):
	cl=Conlimit(x)
	