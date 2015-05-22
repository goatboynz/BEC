
**
** Guide on how to install and use the ts3 plugin.
**

To install and use the Ts3 plugin you need to do some editing first.
You need to open up the file called Ts3_Settings.py in a editor. such as np++ or better ones.
If you already had the Ts3 serverquerier for your Bec. this should be much the same to set up. "maybe easyer"

Ok so here is what you have to edit 1st.

Host 			= "127.0.0.1"	# change if needed
Port			= 10011			# change if needed
User			= "serveradmin" # change if needed
Password		= "SLMufyy9"	# change this
VirtualServer	= 1				# change if needed
Queryname		= "becbot"		# change if want another name..


Next scroll down until you see a variable name like this: Admins
Now as you can see this is a dict. The format we will be using is as following.

Admins = { uid1 : [str/name, int, int, int, int ], uid2 : [str/name, int, int, int, int ] , ...}

the Key is the Uid to the ts3 client you want to notify.
the 4 int's you see are bools on which types of notification a admins will get. 
there are 4 as you can see. we will call them: nok, nob, noh and nfu

nok, Notify on kick
nob, Notify on Ban
noh, Notify on Hack
nfu, Notify From User.

ofcource you need to modify the code somewhat. not to much work. but some python knowlege would be required.


Example i want to have 4 admins.
Admins = {
    'AmIZoqKMye9L4GeBo0EULv4LdqY=' : ["nux", 1 , 1, 1 , 1],  # all
    'BgIZoqdwye0L3GeBo0EWLv5LdqY=' : ["alfred", 1, 0 , 1, 1], # all but not ban
    'ChIZoqaaye1L2GeBo0EXLv6LdqY=' : ["pelle", 0, 1 , 1, ,1], # will notitfy admin on all types except kick,
    'DGIZoqgMye2L1GeBo0EYLv7LdqY=' : ["jonny", 0 , 0 , 1 , 1], # will only be notifyed by users and by hacks
    }
    
    
Bec is set up to ignore some of the kick messages, this can easly be changes.
To change this you need to open up the file called __init__.py
Scroll down and look for the var name called self.BE_msg_ignores.

You can see that there are alots of messages that are ignored. 
self.BE_msg_ignores = [
	"Client not responding",
	"Invalid GUID",
	"Ping too high (",
	"Unknown Game Version",
	"Corrupted Memory #",
	"Global Ban #",
	"Failed to update",
    ....


The reason these messages are ignore is simply to avoid annoying the shit out of the admins on the ts3 about kicks such as Global Ban # etc. its not much they can do about it anyway.

Other than that there is not much more to edit unless you want to expand/modify the plugin, if you deside to modify it you should have some Python knowlege. 
Be sure to match my indentation, you dont want to end up reidenting the hole file.



