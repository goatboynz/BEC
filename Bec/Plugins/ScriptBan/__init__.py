# This plugin will ban a player that has triggered one of the filter rules.
# This plugin is only suted on one mission unless you use common filter files for all your mission.
# To set ban reasons for your rules you need to edit the file. ( reason.py ) 
# You also need to know what ID each rule will have.


import re
import os
import sys
sys.path.append(os.getcwd()+"\\Plugins\\ScriptBan")
import reason

# Define your servers this plugin is to be used on. use config names. leave it empty to start it on all or remove the variable.
SERVERS = ["a2.cfg", "a3.cfg"]

class Restrictions(object):
	
	def __init__(self, instance):
		self.bec = instance
		self.cfgname = self.bec.cfgval.options.filename
		if self.cfgname in SERVERS:
			self.org_func_be_prosess_02	= self.bec._be_prosess_02
			self.bec._be_prosess_02 = self.extend_pros02
			
			################################################################################################################
			### Regular Expressions!.
			################################################################################################################
			self.addbackpackcargo_regex 	= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: addbackpackcargo restriction #(\d+)', re.I)
			self.addmagazinecargo_regex 	= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: addmagazinecargo restriction #(\d+)', re.I)
			self.attachto_regex 			= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: attachto restriction #(\d+)', re.I)
			self.addweaponcargo_regex 		= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: addweaponcargo restriction #(\d+)', re.I)
			self.createvehicle_regex 		= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: createvehicle restriction #(\d+)', re.I)
			self.deletevehicle_regex 		= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: deletevehicle restriction #(\d+)', re.I)
			self.mpeventhandler_regex 		= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: mpeventhandler restriction #(\d+)', re.I)
			self.publicvariable_regex 		= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: publicVariable restriction #(\d+)', re.I)
			self.publicvariableval_regex 	= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: publicVariable value restriction #(\d+)', re.I)
			self.remotecontrol_regex 		= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: remoteControl restriction #(\d+)', re.I)
			self.remoteexec_regex 			= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: remoteExec restriction #(\d+)', re.I)
			self.script_regex 				= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: script restriction #(\d+)', re.I)
			self.selectplayer_regex 		= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: selectplayer restriction #(\d+)', re.I)
			self.setdamage_regex 			= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: setdamage restriction #(\d+)', re.I)
			self.setvariable_regex 			= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: setvariable restriction #(\d+)', re.I)
			self.setvariableval_regex 		= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: setvariable value restriction #(\d+)', re.I)
			self.teamswitch_regex 			= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: teamswitch restriction #(\d+)', re.I)
			self.waypointcondition_regex 	= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: waypointcondition restriction #(\d+)', re.I)
			self.waypointstatement_regex 	= re.compile(r'Player #(\d+) (.+) \((.{32})\) has been kicked by BattlEye: waypointstatement restriction #(\d+)', re.I)
			

	def scriptban(func):
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				self	= args[0]
				sdta 	= args[1]
				command = False
				
				# Addbackpackcargo Restriction
				if self.addbackpackcargo_regex.search(sdta):
					info = self.addbackpackcargo_regex.search(sdta).groups()
					beid = info[0]
					name = info[1]
					guid = info[2]
					tid  = info[3]
					if reason.addbackpackcargo_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.addbackpackcargo_reason[tid]
				
				# Addmagazinecargo Restriction
				elif self.addmagazinecargo_regex.search(sdta):
					info = self.addmagazinecargo_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.addmagazinecargo_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.addmagazinecargo_reason[tid]
				
				# Addweaponcargo Restriction
				elif self.addweaponcargo_regex.search(sdta):
					info = self.addweaponcargo_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.addweaponcargo_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.addweaponcargo_reason[tid]
				
				# Attachto Restriction	
				elif self.attachto_regex.search(sdta):
					info = self.attachto_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.attachto_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.attachto_reason[tid]						
				
				# Createvehicle Restriction
				elif self.createvehicle_regex.search(sdta):
					info = self.createvehicle_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.createvehicle_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.createvehicle_reason[tid]
				
				# Deletevehicle Restriction
				elif self.deletevehicle_regex.search(sdta):
					info = self.deletevehicle_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.deletevehicle_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.deletevehicle_reason[tid]
				
				# Mpeventhandler Restriction
				elif self.mpeventhandler_regex.search(sdta):
					info = self.mpeventhandler_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.mpeventhandler_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.mpeventhandler_reason[tid]
				
				# Publicvariable Restriction
				elif self.publicvariable_regex.search(sdta):
					info = self.publicvariable_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.publicvariable_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.publicvariable_reason[tid]
				
				# Publicvariableval Restriction
				elif self.publicvariableval_regex.search(sdta):
					info = self.publicvariableval_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.publicvariableval_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.publicvariableval_reason[tid]
				
				# Remotecontrol Restriction
				elif self.remotecontrol_regex.search(sdta):
					info = self.remotecontrol_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.remotecontrol_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.remotecontrol_reason[tid]
				
				# Remoteexec Restriction
				elif self.remoteexec_regex.search(sdta):
					info = self.remoteexec_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.remoteexec_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.remoteexec_reason[tid]
					
				# Script Restriction
				elif self.script_regex.search(sdta):
					info = self.script_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.script_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.script_reason[tid]
				
				# Selectplayer Restriction	
				elif self.selectplayer_regex.search(sdta):
					info = self.selectplayer_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.selectplayer_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.selectplayer_reason[tid]
				
				# Setdamage Restriction	
				elif self.setdamage_regex.search(sdta):
					info = self.setdamage_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.setdamage_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.setdamage_reason[tid]
				
				# Setvariable Restriction
				elif self.setvariable_regex.search(sdta):
					info = self.setvariable_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.setvariable_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.setvariable_reason[tid]
				
				# Setvariableval Restriction
				elif self.setvariableval_regex.search(sdta):
					info = self.setvariableval_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.setvariableval_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.setvariableval_reason[tid]
				
				# Teamswitch Restriction
				elif self.teamswitch_regex.search(sdta):
					info = self.teamswitch_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.teamswitch_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.teamswitch_reason[tid]
				
				# Waypointcondition Restriction	
				elif self.waypointcondition_regex.search(sdta):
					info = self.waypointcondition_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.waypointcondition_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.waypointcondition_reason[tid]
				
				# Waypointstatement Restriction		
				elif self.waypointstatement_regex.search(sdta):
					info = self.waypointstatement_regex.search(sdta).groups()
					guid = info[2]
					tid  = info[3]
					if reason.waypointcondition_reason.has_key(tid):
						command = "addban "+guid+" 0 BEC : "+reason.waypointstatement_reason[tid]
					
				# Send the ban command..
				if command:
					self.bec._Bec_queuelist.append(command)

		return extended_data		
	
	@scriptban
	def extend_pros02(self, data):
		self.org_func_be_prosess_02(data)
		
# function bec will use to start the plugin
def start(x):
	Restrictions(x)
	