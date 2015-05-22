This is the Plugin directory for Bec.

The File called __init__.py MUST NOT BE DELETED. 

The plugins you want to be running neend to be a directory.

Plugin / Directory layout.
Example:

>/Bec/Plugins
		|
		| > __init__.py
		|
		| > Ts3
		|	|
		|	|> __init__.py
		|	|> Ts3Classes.py
		|	|> Ts3Settings.py
		|
		| > Rss
		|	|
		|	|> __init__.py
		|	|> feedparser.py
		|
		| > MySQLdb
		|	|
		|	|> __init__.py
		|	|> whatever.py
		|
		| > Amp server
		|	|
		|	|> __init__.py
		|	|> more_files.py
		|	
		| > Your Plugin
			|
			|> __init__.py

To remove/uninstall a plugin you just delete the plugin directory you like to remove.
To disable all plugins, you just delete\remove\rename the plugins dir in root of bec "bec\plugins"
