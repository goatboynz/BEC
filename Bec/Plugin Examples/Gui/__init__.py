# Super Simple UI example


import sys
import os
import wx
import wx.xrc

from twisted.internet import reactor
from twisted.internet import task

sys.path.append(os.getcwd()+"\\Plugins\\Gui")
import gui

class Base_Gui(gui.bec_gui):
	def __init__(self, instance):
		self.bec = instance
		gui.bec_gui.__init__(self, parent=None, )

		self.indx = -1 # index of selection in the player list
		self.beid = -1 # beid.. set to -1 for none.
		
		##################################################
		# Set up the listbox ctrl
		self.PlayerCtrl.InsertColumn(0,'Id')
		self.PlayerCtrl.SetColumnWidth(0, 35)
		self.PlayerCtrl.InsertColumn(1,'Guid')
		self.PlayerCtrl.SetColumnWidth(1, 150)
		self.PlayerCtrl.InsertColumn(2,'Name')
		self.PlayerCtrl.SetColumnWidth(2, 100)
		self.PlayerCtrl.InsertColumn(3,'Ip')
		self.PlayerCtrl.SetColumnWidth(3, 100)
		self.PlayerCtrl.InsertColumn(4,'Connected')
		self.PlayerCtrl.SetColumnWidth(4, 90)
		self.PlayerCtrl.InsertColumn(5,'Status')		
		self.PlayerCtrl.SetColumnWidth(5, 75)		
		
		
		##################################################
		# Main Binds..
		
		# Send cmd when enter is press in text area.
		self.Bind(wx.EVT_TEXT_ENTER, self.WXEvent_CmdSend, self.inputCtrl)			
		
		# Send command when the button is pressed.
		self.Bind(wx.EVT_BUTTON, self.WXEvent_CmdSend, self.sendButton)
		
		# set index, and beid or selected player on lmb
		self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.WXEvent_PlayerListMenu_RMB, self.PlayerCtrl)
		
		# create menu with rmb.
		self.Bind(wx.EVT_COMMAND_LEFT_CLICK, self.WXEvent_PlayerListMenu_LMB, self.PlayerCtrl)
		
		# The X. Close window button pressed. 
		self.Bind(wx.EVT_CLOSE, self.WXEvent_closewindow)
		
		##################################################
		# Create menus in playerlist
		self.createPlayerListMenu()			
		
		##################################################
		# Task to populate the Player list box
		self.populate_playerlist_Task = task.LoopingCall(self.populate_playerlist)
		self.populate_playerlist_Task.start(3, False)


	def kick(self, event):
		cmd = "kick "+str(self.beid)
		self.bec._Bec_queuelist.append(cmd)
	def ban(self,event):
		cmd = "ban "+str(self.beid)
		self.bec._Bec_queuelist.append(cmd)
	
	def createPlayerListMenu(self):
		self.playerlistmenu = wx.Menu()
		item1 = self.playerlistmenu.Append(-1,'Kick', 'Kick player from the server')
		item2 = self.playerlistmenu.Append(-1,'Ban', 'Ban the player')

		# Binds for player list menu.
		self.Bind(wx.EVT_MENU, self.kick, item1)
		self.Bind(wx.EVT_MENU, self.ban, item2)	
	def populate_playerlist(self):
		''' 
			this is not the best way to populate the list.
			using DeleteAllItems() will cause a short flash on update.
			best is just to compare two dicts "Bec_playersconnected" and a tmp
			to see which player is no longer connecter, or if new players has connected.
			then just delete/change the row of the menu items
		'''
		
		row = 0
		self.PlayerCtrl.DeleteAllItems()
		for gkey in self.bec._Bec_playersconnected.keys():
			
			#self.PlayerCtrl.DeleteItem(row)
			beid = self.bec._Bec_playersconnected[gkey][0]
			nick = self.bec._Bec_playersconnected[gkey][1]
			ip  = self.bec._Bec_playersconnected[gkey][2]
			ctime = self.bec._Bec_playersconnected[gkey][3].strftime("%H:%M:%S %d.%m")
			status = self.bec._Bec_playersconnected[gkey][4]
			
			if status == 0:
				status = "Lobby"
			else:
				status = "Ingame"

			self.PlayerCtrl.InsertStringItem(row,str(beid))
			self.PlayerCtrl.SetStringItem(row,1,str(gkey))
			self.PlayerCtrl.SetStringItem(row,2,str(nick))
			self.PlayerCtrl.SetStringItem(row,3,str(ip))
			self.PlayerCtrl.SetStringItem(row,4,str(ctime))
			self.PlayerCtrl.SetStringItem(row,5,str(status))
			row +=1		
	
	##################################################
	# Events.
	def WXEvent_CmdSend(self, event):
		cmd = self.inputCtrl.GetValue()
		self.bec._Bec_queuelist.append(cmd)
		self.inputCtrl.SetValue("")		
	def WXEvent_closewindow(self,event):
		self.populate_playerlist_Task.stop() # Stop task for populate guid list.
		self.Destroy()
	def WXEvent_PlayerListMenu_LMB(self, event):
		'''this will just set the index and beid of selected player'''
		self.beid = -1
		indx = self.PlayerCtrl.GetFirstSelected()
		if indx != -1:
			self.indx = indx	
			self.beid = self.PlayerCtrl.GetItem(self.indx, 0).GetText()
	def WXEvent_PlayerListMenu_RMB(self,event):
		''' this will create the menu when right button pressed'''
		self.beid = -1
		indx = self.PlayerCtrl.GetFirstSelected()
		if indx != -1:
			self.indx = indx
			self.beid = self.PlayerCtrl.GetItem(self.indx, 0).GetText()
			
			position = self.ScreenToClient(wx.GetMousePosition())
			self.PopupMenu(self.playerlistmenu, position)


		
def start(x):

	app = wx.App(False)
	frame = Base_Gui(x)
	frame.Show()
	app.MainLoop()
	#reactor.registerWxApp(app)

	
	