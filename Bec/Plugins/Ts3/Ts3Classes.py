# -*- encoding: utf-8 -*-
import sys
import time
import telnetlib
import logging
import thread
from threading import Lock

# Python TS3 Library (python-ts3)
#
# Copyright (c) 2011, Andrew Williams
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



# HostMessageMode #
HOST_MESSAGE_MODE_LOG = 1 		# 1: display message in chatlog
HOST_MESSAGE_MODE_MODAL = 2 	# 2: display message in modal dialog
HOST_MESSAGE_MODE_MODALQUIT = 3 # 3: display message in modal dialog and close connection
# CodecType #
CODEC_SPEEX_NARROWBAND = 0 		# 0: speex narrowband     (mono, 16bit, 8kHz)
CODEC_SPEEX_WIDEBAND = 1 		# 1: speex wideband       (mono, 16bit, 16kHz)
CODEC_SPEEX_ULTRAWIDEBAND = 2 	# 2: speex ultra-wideband (mono, 16bit, 32kHz)
CODEC_CELT_MONO = 3 			# 3: celt mono (mono, 16bit, 48kHz)
# CodecEncryption #
CODEC_CRYPT_INDIVIDUAL = 0 		# 0: configure per channel
CODEC_CRYPT_DISABLED = 1 		# 1: globally disabled
CODEC_CRYPT_ENABLED = 2 		# 2: globally enabled
# TextMessageTarget #
TEXT_MESSAGE_TARGET_CLIENT = 1 	# 1: target is a client
TEXT_MESSAGE_TARGET_CHANNEL = 2 # 2: target is a channel
TEXT_MESSAGE_TARGET_SERVER = 3 	# 3: target is a virtual server
# LogLevel #
LOGLEVEL_ERROR = 1 				# 1: everything that is really bad
LOGLEVEL_WARNING = 2 			# 2: everything that might be bad
LOGLEVEL_DEBUG = 3  			# 3: output that might help find a problem
LOGLEVEL_INFO = 4 				# 4: informational output
# ReasonIdentifier #
REASON_KICK_CHANNEL = 4 		# kick client from channel
REASON_KICK_SERVER = 5 			# kick client from server
# PermissionGroupDatabaseTypes #
PERMGROUP_DBTYPE_TEMPLATE = 0 	# template group (used for new virtual servers)
PERMGROUP_DBTYPE_REGULAR = 1 	# regular group (used for regular clients)
PERMGROUP_DBTYPE_QUERY = 2 		# global query group (used for ServerQuery clients)
# PermissionGroupTypes #
PERMGROUP_TYPE_SERVERGROUP = 0 		# server group permission
PERMGROUP_TYPE_GLOBALCLIENT = 1 	# client specific permission
PERMGROUP_TYPE_CHANNEL = 2 			# channel specific permission
PERMGROUP_TYPE_CHANNELGROUP = 3 	# channel group permission
PERMGROUP_TYPE_CHANNELCLIENT = 4 	# channel-client specific permission
# TokenType #
TOKEN_SERVER_GROUP = 0 		# server group token (id1={groupID} id2=0)
TOKEN_CHANNEL_GROUP = 1 	# channel group token (id1={groupID} id2={channelID})
# PermissionAutoUpdateTypes #
PERMISSION_AUTOUPDATE_QG = 0 # 0: target will be handled as Query Guest
PERMISSION_AUTOUPDATE_QA = 1 # 1: target will be handled as Query Admin
PERMISSION_AUTOUPDATE_SA = 2 # 2: target will be handled as Server Admin
PERMISSION_AUTOUPDATE_SN = 3 # 3: target will be handled as Server Normal
PERMISSION_AUTOUPDATE_SG = 4 # 4: target will be handled as Server Guest
PERMISSION_AUTOUPDATE_CA = 5 # 5: target will be handled as Channel Admin
PERMISSION_AUTOUPDATE_CO = 6 # 6: target will be handled as Channel Operator
PERMISSION_AUTOUPDATE_CV = 7 # 7: target will be handled as Channel Voice
PERMISSION_AUTOUPDATE_CG = 8 # 8: target will be handled as Channel Guest

ts3_escapechar = [
	(chr(92), r'\\'),  # \
	(chr(47), r"\/"),  # /
	(chr(32), r'\s'),  # Space
	(chr(124), r'\p'), # |
	(chr(7), r'\a'),   # Bell
	(chr(8), r'\b'),   # Backspace
	(chr(12), r'\f'),  # Formfeed
	(chr(10), r'\n'),  # Newline
	(chr(13), r'\r'),  # Carrage Return
	(chr(9), r'\t'),   # Horizontal Tab
	(chr(11), r'\v'),  # Vertical tab
]


class ConnectionError(Exception):
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
	def __str__():
		return 'Error connecting to host %s port %s.' % (self.ip, self.port,)
class NoConnection(Exception):
	def __str__():
		return 'No connection established.' % (self.ip, self.port,)
class InvalidArguments(ValueError):
	'''Raised when received invalid arguments'''
class TS3Response(object):
	def __init__(self, response, data):
		self.response = TS3Protocol.parse_response(response)
		self.data = TS3Protocol.parse_data(data)

		if isinstance(self.data, dict):
			if self.data:
				self.data = [self.data]
			else:
				self.data = []
	@property
	def is_successful(self):
		return self.response['msg'] == 'ok'
class TS3Protocol(object):
	#io_lock = Lock()
	@property
	def logger(self):
		if not hasattr(self, "_logger"):
			self._logger = logging.getLogger(__name__)
		return self._logger
	def connect(self, ip, port=10011, timeout=10):
		#self.io_lock.acquire()
		try:
			self._telnet = telnetlib.Telnet(ip, port)
		except telnetlib.socket.error:
			# Release the lock if there was an error.
			#self.io_lock.release()
			raise ConnectionError(ip, port)
			
		self._timeout = timeout
		self._connected = False
		data = self._telnet.read_until("\n\r", self._timeout)
		#self.io_lock.release()

		if data.endswith("TS3\n\r"):
			self._connected = True
		return self._connected
	def disconnect(self):
		self.check_connection()
		self.send_command("quit")
		self._telnet.close()
		self._connected = False
	def send_command(self, command, keys=None, opts=None):
		self.check_connection()
		commandstr = self.construct_command(command, keys=keys, opts=opts)
		self.logger.debug("send_command - %s" % commandstr)
		#self.io_lock.acquire()
		self._telnet.write("%s\n\r" % commandstr)
		data = ""
		response = self._telnet.read_until("\n\r", self._timeout)
		#self.io_lock.release()
		if not response.startswith("error"):
			# what we just got was extra data
			data = response
			response = self._telnet.read_until("\n\r", self._timeout)
		return TS3Response(response, data)
	def check_connection(self):
		if not self.is_connected:
			raise NoConnectionError
	def is_connected(self):
		return self._connected
	def construct_command(self, command, keys=None, opts=None):
		cstr = [command]
		# Add the keys and values, escape as needed        
		if keys:
			for key in keys:
				if isinstance(keys[key], list):
					ncstr = []
					for nest in keys[key]:
						ncstr.append("%s=%s" % (key, self._escape_str(nest)))
					cstr.append("|".join(ncstr))
				else:
					cstr.append("%s=%s" % (key, self._escape_str(keys[key])))

		# Add in options
		if opts:
			for opt in opts:
				cstr.append("-%s" % opt)

		return " ".join(cstr)
	
	@staticmethod
	def parse_response(response):
		return TS3Server.parse_data(response[6:])
    
	@staticmethod
	def parse_data(data):
		data = data.strip()
		multipart = data.split('|')

		if len(multipart) > 1:
			values = []
			for part in multipart:
				values.append(TS3Protocol.parse_data(part))
			return values

		chunks = data.split(' ')
		parsed_data = {}

		for chunk in chunks:
			chunk = chunk.strip().split('=')
			if len(chunk) > 1:
				if len(chunk) > 2:
					# value can contain '=' which may confuse our parser
					chunk = [chunk[0], '='.join(chunk[1:])]
                
				key, value = chunk
				parsed_data[key] = TS3Protocol._unescape_str(value)
			else:
				# TS3 Query Server may sometimes return a key without any value
				# and we default its value to None
				parsed_data[chunk[0]] = None
		return parsed_data        

	@staticmethod
	def _escape_str(value):
		if isinstance(value, int):
			return str(value)
        
		for i, j in ts3_escapechar:
			value = value.replace(i, j)
        
		return value

	@staticmethod
	def _unescape_str(value):
		if isinstance(value, int):
			return str(value)
        
		for i, j in ts3_escapechar:
			value = value.replace(j, i)
		return value
class TS3Server(TS3Protocol):
	def __init__(self, ip=None, port=10011, id=0):
		if ip and port:
			if self.connect(ip, port) and id > 0:
				self.use(id)
	@property
	def logger(self):
		if not hasattr(self, "_logger"):
			self._logger = logging.getLogger(__name__)
		return self._logger
	def login(self, username, password):
		"""
			Login to the TS3 Server
			@param username: Username
			@type username: str
			@param password: Password
			@type password: str
		"""
		response = self.send_command('login', keys={'client_login_name': username, 'client_login_password': password })
		return response.is_successful
	def serverlist(self):
		"""
			Get a list of all Virtual Servers on the connected TS3 instance
		"""
		return self.send_command('serverlist')
	def use_vs(self, id):
		"""
			Use a particular Virtual Server instance
			@param id: Virtual Server ID
			@type id: int
		"""
		response = self.send_command('use', keys={'sid': id})
		return response.is_successful
	def clientlist(self):
		"""
			Returns a clientlist of the current connected server/vhost
		"""
		response = self.send_command('clientlist')
		if response.is_successful:
			clientlist = {}
			for client in response.data:
				clientlist[client['clid']] = client
			return clientlist
		else:
			# TODO: Raise a exception?
			self.logger.debug("clientlist - error retrieving client list")
			return {}
	def clientinfo(self):
		'''return info on clients'''
		clientlist = self.clientlist()
		clients = {}
		i = 0
		for k in clientlist.keys():
			#print clientlist[k]
			name = clientlist[k]["client_nickname"]
			clid = clientlist[k]["clid"]
			res = self.send_command('clientinfo', keys={'clid': clid})
			if res.is_successful:
				dta = res.data
				name = dta[0]['client_nickname']
				ip	 = dta[0]['connection_client_ip']
				cid  = dta[0]['cid'] # get channel id

				#channel = dta[0]['connection_client_ip']
				clients[i] = [name,ip,cid]
				
				i += 1
		return clients
	def channellist(self):
		'''doc'''
		res = self.send_command('channellist')
		if res.is_successful:		
			dta = res.data
			return dta
	def clientban(self, player_ip, name, message=None):
		clientlist = self.clientlist()
		for k in clientlist.keys():
			name = clientlist[k]["client_nickname"]
			clid = clientlist[k]["clid"]
			res = self.send_command('clientinfo', keys={'clid': clid})
			if res.is_successful:
				dta = res.data
				name = dta[0]['client_nickname']
				ip	 = dta[0]['connection_client_ip']
				if player_ip == ip:
					if not message:
						message = ''
					else:
						# Kick message can only be 40 characters
						message = message[:40]
					#banclient clid={clientID} [time={timeInSeconds}] [banreason={text}]
					response = self.send_command('banclient', keys={'time': 0, 'banreason': message, 'clid': clid, })
					return response.is_successful
		return False
	def clientkick(self, player_ip, name, type=REASON_KICK_SERVER, message=None):
		clientlist = self.clientlist()
		for k in clientlist.keys():
			name = clientlist[k]["client_nickname"]
			clid = clientlist[k]["clid"]
			res = self.send_command('clientinfo', keys={'clid': clid})
			if res.is_successful:
				dta = res.data
				name = dta[0]['client_nickname']
				ip	 = dta[0]['connection_client_ip']
				if player_ip == ip:
					if not message:
						message = ''
					else:
						# Kick message can only be 40 characters
						message = message[:40]
					response = self.send_command('clientkick', keys={'reasonid': type, 'reasonmsg': message, 'clid': clid, })
					return response.is_successful
		return False
	def clientpoke(self, clid, message):
		"""
			Poke a client with the specified message
		"""

		response = self.send_command('clientpoke', keys={'clid': clid, 'msg': message})
		return response.is_successful
	def send_client_message(self, player_ip, message, type="pm"):
		'''doc'''
		clientlist = self.clientlist()
		for k in clientlist.keys():
			name = clientlist[k]["client_nickname"]
			clid = clientlist[k]["clid"]
			res = self.send_command('clientinfo', keys={'clid': clid})
			if res.is_successful:
				dta = res.data
				name = dta[0]['client_nickname']
				ip	 = dta[0]['connection_client_ip']
				if player_ip == ip:
					if type == "poke":
						self.clientpoke(clid, message)
					elif type == "pm":
						self.send_command('sendtextmessage', keys={'targetmode' : TEXT_MESSAGE_TARGET_CLIENT, 'target' : clid , 'msg' : message})
					break
	def send_admin_message(self, adminlist, message):
		try:
			clientlist = self.clientlist()
			for k in clientlist.keys():
				#name = clientlist[k]["client_nickname"]
				clid = clientlist[k]["clid"]
				res = self.send_command('clientinfo', keys={'clid': clid})
				if res.is_successful:		
					dta = res.data
					#name = dta[0]['client_nickname']
					ip	 = dta[0]['connection_client_ip']				
					uid	 = dta[0]['client_unique_identifier']
					if adminlist.has_key(uid):
						self.send_command('sendtextmessage', keys={'targetmode' : TEXT_MESSAGE_TARGET_CLIENT, 'target' : clid , 'msg' : message})
		except:
			return False
	def send_global_message(self, msg):
		"""
			Send a global message to the current Virtual Server
			@param msg: Message
		"""
		response = self.send_command('gm', keys={'msg': msg})
		return response.is_successful
	def query_name_changer(self, name):

		#clientupdate client_nickname=ScP\s(query)
		self.send_command('clientupdate', keys={'client_nickname' : name})	
