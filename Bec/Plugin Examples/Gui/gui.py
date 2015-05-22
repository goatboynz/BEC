# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE UNLESS YOU KNOW WHAT YOU ARE DOING!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class bec_gui
###########################################################################

class bec_gui ( wx.Frame ):
	
	def __init__( self, parent ):
		FrameTitle = self.bec.Bec_Cfg_Main_LogDirName
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = FrameTitle, pos = wx.DefaultPosition, size = wx.Size( 500,397 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 500,72 ), wx.Size( -1,-1 ) )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText10 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"command", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText10.Wrap( -1 )
		bSizer8.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		self.inputCtrl = wx.TextCtrl( self.m_panel2, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer8.Add( self.inputCtrl, 1, wx.ALL, 5 )
		
		self.sendButton = wx.Button( self.m_panel2, wx.ID_ANY, u"send", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer8.Add( self.sendButton, 0, wx.ALL, 5 )
		
		
		self.m_panel2.SetSizer( bSizer8 )
		self.m_panel2.Layout()
		bSizer8.Fit( self.m_panel2 )
		bSizer7.Add( self.m_panel2, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.PlayerCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_AUTOARRANGE|wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES )
		bSizer3.Add( self.PlayerCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer7.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

