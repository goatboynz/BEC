This plugin will ban a player that triggeres one of the filter rules in BE.
This plugin is only suted on one mission unless you use common filter files for all your mission or modify the plugin.
To set ban reasons for your rules you need to edit the file. ( reason.py ) 
You also need to know what ID each rule will have.

To install/start the plugin simply open up the __init__.py file and edit the variable called: SERVERS
in this variable put in your config name. example
SERVERS = ["MyArmA3.cfg"]


As an example.
if a player gets kicked of by "RemoteExec Restriction #1"
and your rules for that filter in reason.py is like 

# Remoteexec Restriction
remoteexec_reason = {
 "0" : "go home kiddie", 
 "1" : "Better luck next time" 
}

He will then be added to your ban file with reason: "Better luck next time"



to uninstall this plugin. just remove the ScriptBan directory. or edit the start function in __init__.py
