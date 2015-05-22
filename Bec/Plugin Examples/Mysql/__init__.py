import MySQLdb


## Get the MySQLdb module source from here .
## http://sourceforge.net/projects/mysql-python/files/mysql-python/1.2.3/MySQL-python-1.2.3.tar.gz/download

## or get the installer from this page. MySQL-python-1.2.4.win32-py2.6.‌exe
## http://www.lfd.uci.edu/~gohlke/pythonlibs/ 

##  MySQL-python-1.2.4 is included in Bec.lib to allow this example to be used.


# This is a simple example on how to use mysql with Bec.
# it does not take into account .escape_string 
# if you deside to make your own mysql plugin you need to take this into account to prevent sql injections
# may also want to take a look at cursor.executemany if needed.


# This will basicly show you how to create a simple mysql query and extend the unverified function in bec "Extend & Monkey patch".
# bec will send a query request to mysql with the player guid when a player connect and gets unverified.
# the query will return 1 or 0. "True or False" , if the result is True the player gets kicked out of the server.



class Bec_Mysql(object):
	def __init__(self):
		
		self.HOST = "127.0.0.1"
		self.PORT = 3306
		self.USER = "Bec"
		self.PASS = "123456"
		self.TABLE = "bans"
		self.DATABASE = "BecTestDatabase"

		# Connect.
		self.db = self.connect()
		
	def connect(self):
		db=""
		#try:

		db = MySQLdb.connect(self.HOST, self.USER, self.PASS, self.DATABASE)
		#except:
		#	print "Error: Can not connect to MySql Host\nCheck config file for correct values"
		return db	
	def check_guid(self, guid):
		
		result = False
		cursor = self.db.cursor()
		sql = "SELECT Guid FROM `%s` WHERE Guid = '%s' Limit 1" % (self.TABLE, guid)
		cursor.execute(sql)

		while (1):
			row = cursor.fetchone()
			if row == None:
				break

			if (row[0] == guid):
				result = True
				break
		return result
	
	'''
	def keepalive(self):
		status = 0
		if self.db:
			try:
				self.db.ping()
				status = 1
			except:
				status = 0
		return status	
	def insert_ban(self, guid, nick, reason):

		cursor = self.db.cursor()	
		sql = "INSERT INTO %s (GUID,NICK,REASON) VALUES ('%s', '%s', '%s', %s, '%s' )" % (self.TABLE, guid, nick, reason)
		try:
			cursor.execute(sql)
			self.db.commit()
		except:
			self.db.rollback()
	'''
	def close(self):
		self.db.close()

class Bec_MysqlHandler(object):
	def __init__(self, instance):
	
		self.bec = instance
		self.MySqlObj = Bec_Mysql()
		
		# Extend & monkey patch Bec functions..
		self.org_func_unverified = self.bec._be_unverified		
		self.bec._be_unverified	 = self.unverified

	def Be_PlayerUnVerified(func):
		'''
			This will extend the verified function
			Add your extra code into extended_data -> finally.
		
			Arg 0 can be considered as self.
			Arg 1 will be a regex obj		
		'''
		def extended_data(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			finally:
				

				self = args[0]
				vdata = args[1].groups()

				guid = vdata[2]
				beid = vdata[0]
				nick = vdata[1]
				
				banned = self.MySqlObj.check_guid(guid)
				if banned:
					cmd = "kick "+str(beid)+" Get lost."
					self.bec._Bec_queuelist.append(cmd)
		return extended_data		

	@Be_PlayerUnVerified
	def unverified(self,data):
		'''This is a monkey patched function which uses a decorator to extends the orginale function'''
		self.org_func_unverified(data)


# function to start the plugin.		
def start(i):

	Bec_MysqlHandler(i)