************************************************************************************************
## About the Status plugin:


The Status plugin is in a way a mix of Battleye and Gamespy serverinfo.
This plugin will create a xml status file for the current Bec session.
How often this file is created is set in the settings file.
You are also able to uploade the xml to a remote host by the ftp protocol.

visit http://www.jointheriot.org/viewpage.php?page_id=9 to see how it may look when integrated into the webpage.


************************************************************************************************
## Guide on how to install and use the Status plugin:


To install and use the Status plugin you need to do some editing first.
You need to open up the file called Status_Settings.py in a editor. such as np++ or better ones.


Ok so here is what you have to edit 1st.

look for SERVERS = [ SERVER1, SERVER2 ] ,now this needs to be changes to the config name(s) you use to start up Bec. 
if you start bec like. Bec.exe -f MyServer.cfg , then do it like: SERVER1 = "MyServer.cfg"

In the SERVERS list, you set it like: 
SERVERS = [SERVER1]

Next scroll down until you can see

if SERVER1:
	...
	...
elif SERVER2:
	...
	...
else
	return False
	
	
Now you need to set the correct settings in there. if you want to use ftp you need to fill out all the userdata..
Make sure to read the comments in the Settings.py file, sice they explains what the var's do.
Xml files will still be created if you deside not to use Ftp.
The Xml file(s) will be created and saved into the directory called "Reports" in the Status plugin.



************************************************************************************************
## Credits:
Sup@hKing for the idea of the Status plugin and for testing and reporting issues during development.

************************************************************************************************
## Bugs:
im sure there are some!..

