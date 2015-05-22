
class Dynamic_CfgValues(object):
	''' Example class on how to get/set Bec config values.'''
	def __init__(self, instance):
		'''
			Change Becs config values while bec is running instead of restarting bec.
			
			--------------------------------------------------------------------------------------------------------------
			** Basic config settings **
			
			instance.Bec_Cfg_Misc_AsciiNickOnly	= bool .. allow/disallow players with none ascii names
			instance.Bec_Cfg_Misc_AsciiChatOnly	= bool .. allow/disallow players with none ascii chat	
			instance.Bec_Cfg_Misc_IngoreChatChars = string .. ignore some symboles with asciiChat only
			
			instance.Bec_Cfg_Misc_ServerExe	= string (name of server exe) usally not needed.
			* This value is used during startup and is in use before the plugins are loaded so no point in trying to change it.
			
			instance.Bec_Cfg_Misc_NickFilterFile = txt file | abs or relative inc filename .. kick rude nicks.
			* This file is read into mem before the plugins are loaded so no point in trying to change it.
			  instead change the instance._Bec_unvalidnicks (type list) with elements of names
			
			instance.Bec_Cfg_Misc_WordFilterFile = txt file | abs or relative path filename .. rude words.
			* This file is read into mem before the plugins are loaded so no point in trying to change it.
			  instead change the instance._Bec_unwantedwords (type list) with elements of words
			
			instance.Bec_Cfg_Misc_SchedulerFile = xml file | abs or relative path filename .. scheduler definations.
			* This file is read before the plugins are loaded so no point in trying to change it.
			
			instance.Bec_Cfg_Misc_WhiteListFile	= txt file | abs or relative path inc filename
			* This file is read into mem before the plugins are loaded so no point in trying to change it.
			  instead change the instance._Bec_whitelist (type list) with elements of guids
			
			instance.Bec_Cfg_Misc_WhileListKickMsg = string
			instance.Bec_Cfg_Misc_Warnings = int .. max warnings before kick occures.
			
			* These console values are read into mem before the plugins are loaded so no point in trying to change it.
			* unless you make a function to refresh the console
			instance.Bec_Cfg_Misc_Console_Color  = int .. Color or rcon console.
			instance.Bec_Cfg_Misc_Console_Height = int .. min 1
			instance.Bec_Cfg_Misc_Console_Width  = int .. 14 min
			
			instance.Bec_Cfg_Misc_Timeout = int .. Timeout bec will wait for the armaserver and or the socket
			* No point in changing this as its used during the startup.
			
			instance.Bec_Cfg_Misc_KickLobbyIdlers         = int .. Kick lobby idlers disabled by default
			instance.Bec_Cfg_Misc_MaxPlayerNameLength     = int ..  Limit player name length
			instance.Bec_Cfg_Misc_DisallowPlayerNameChars = string .. Disallow certan chars in player name
			instance.Bec_Cfg_Misc_ChatChannelFiles        = bool .. log chat channels to channel files set off by default
			instance.Bec_Cfg_Misc_SlotLimit               = int
			instance.Bec_Cfg_Misc_SlotLimit_Msg           = string
			
			--------------------------------------------------------------------------------------------------------------
			** Antispam Values **

			instance.Bec_Cfg_ChatSpam = bool .. Disable/Enable Antispam
			
			instance.Bec_Cfg_ChatSpam_Lobby	           = int
			instance.Bec_Cfg_ChatSpam_Lobby_Time_Lower = int
			instance.Bec_Cfg_ChatSpam_Lobby_Time_Upper = int > Lower 
			
			instance.Bec_Cfg_ChatSpam_Global            = int
			instance.Bec_Cfg_ChatSpam_Global_Time_Lower = int
			instance.Bec_Cfg_ChatSpam_Global_Time_Upper = int > Lower
			
			instance.Bec_Cfg_ChatSpam_Side            = int
			instance.Bec_Cfg_ChatSpam_Side_Time_Lower = int
			instance.Bec_Cfg_ChatSpam_Side_Time_Upper = int > Lower
			
			instance.Bec_Cfg_ChatSpam_Group            = int
			instance.Bec_Cfg_ChatSpam_Group_Time_Lower = int
			instance.Bec_Cfg_ChatSpam_Group_Time_Upper = int > Lower
			
			instance.Bec_Cfg_ChatSpam_Vehicle            = int
			instance.Bec_Cfg_ChatSpam_Vehicle_Time_Lower = int
			instance.Bec_Cfg_ChatSpam_Vehicle_Time_Upper = int > Lower
			
			instance.Bec_Cfg_ChatSpam_Command            = int
			instance.Bec_Cfg_ChatSpam_Command_Time_Lower = int
			instance.Bec_Cfg_ChatSpam_Command_Time_Upper = int > Lower
			
			instance.Bec_Cfg_ChatSpam_Commander            = int
			instance.Bec_Cfg_ChatSpam_Commander_Time_Lower = int
			instance.Bec_Cfg_ChatSpam_Commander_Time_Upper = int > Lower
			
			instance.Bec_Cfg_ChatSpam_Direct            = int
			instance.Bec_Cfg_ChatSpam_Direct_Time_Lower = int
			instance.Bec_Cfg_ChatSpam_Direct_Time_Upper = int > Lower
			
			--------------------------------------------------------------------------------------------------------------
			** Chat Restriction **

			* -1 disabled, 0 instant kick, 1 does 1 warning before kick.
			instance.Bec_Cfg_Chat_Lobby     = int
			instance.Bec_Cfg_Chat_Global    = int
			instance.Bec_Cfg_Chat_Side      = int
			instance.Bec_Cfg_Chat_Group     = int
			instance.Bec_Cfg_Chat_Vehicle   = int
			instance.Bec_Cfg_Chat_Command   = int
			instance.Bec_Cfg_Chat_Commander = int
			instance.Bec_Cfg_Chat_Direct    = int
		'''
		self.bec = instance
		
	def get_cfg_asciinick(self):
		''' Get the value of config value AsciiNickOnly '''
		return self.bec.Bec_Cfg_Misc_AsciiNickOnly
	def set_cfg_asciinick(self, bool):
		''' Set the value of config value AsciiNickOnly '''
		self.bec.Bec_Cfg_Misc_AsciiNickOnly = bool
		
	def get_cfg_asciichat(self):
		''' Get the value of config value AsciiChatOnly '''
		return self.bec.Bec_Cfg_Misc_AsciiChatOnly
	def set_cfg_asciichat(self, bool):
		''' Set the value of config value AsciiChatOnly '''
		self.bec.Bec_Cfg_Misc_AsciiChatOnly = bool

def start(i):
	''' Main start function for the plugin '''
	dynobj = Dynamic_CfgValues(i)
	
	''' just toggle a setting '''
	if dynobj.get_cfg_asciichat():
		dynobj.set_cfg_asciichat(False)
		print dynobj.get_cfg_asciichat()
	else:
		dynobj.set_cfg_asciichat(True)
		print dynobj.get_cfg_asciichat()
		
	
