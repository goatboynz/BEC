from twisted.internet import task
import psutil

Server1 = "a3.cfg"
Server2 = "My_Server2_Conf_Name.cfg"

SERVERS = [Server1, Server2]
def shutdown(pid):
	try:
		pros=psutil.Process(pid)
		pros.terminate()
	except:
		print "error shuting down the server"
	
def start(x):
	bec = x
	
	# interval takes secs seconds.
	interval = 60 * 60 * 4 # <- = 4 hours
	
	# start the task
	shutdown_task = task.LoopingCall(shutdown, bec.armapid)
	
	# call the task after N secs
	shutdown_task.start(interval, False)
