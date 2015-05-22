# -*- encoding: utf-8 -*-
__version__ 		= "0.2"
__license__ 		= "Gpl v2"
__copyright__ 		= "Copyright 2013, Stian Mikalsen"
__author__ 			= "Stian Mikalsen"
__description__ 	= 'Simple RSS feed collector'
__author_email__	= "stianmikalsen@hotmail.com"
__maintainer__ 		= "Stian Mikalsen"

import sys
import os
import time
from Lib.BecClasses import Timec
from Lib.Bec_Console_Colors import Cprint

sys.path.append(os.getcwd()+"\\Plugins\\Rss")
import feedparser

class rss_handler(object):
	def __init__(self, instance):
		self.bec = instance

		# set the wanted rss url.
		self.url = "http://www.armaholic.com/rss.php"
		
		# start the show function.
		self.rss_show()

	def rss_show(self):
		''' Function to collect and show 10 latest rss news from set url'''
		try:
			while True:
		
				# Collect the rss titles.
				feed = feedparser.parse(self.url)
				status = feed.status
			
				if status == 200:
			
					entries = feed.entries
					rssnews = []
					for e in entries:
						rssnews.append(e.title)
						if len(rssnews) == 10:
							break

				
					# show the news to players with 15 sec interval between the news titles.
					for i in range(0, len(rssnews)):
						time.sleep(15)
						rcon_msg = "say -1 ArmaHolic News: "+ rssnews[i]
						self.bec._Bec_queuelist.append(rcon_msg)

				else:
					Cprint().default(Timec().GetTime()+" : Problems collecting Rss News : Error : "+str(status)+ " : Maybe Url is wrong or Rss Host is down" )
			
				# Wait 1.5 our before collecting news again.
				time.sleep(5400)
		except:
			Cprint().default(Timec().GetTime()+" : Problems collecting Rss News : Error")
	
			
def start(i):
	rssobj = rss_handler(i)

