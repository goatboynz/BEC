

This is just a quick and dirty example on howto use the SOME of the wx module with Bec.
i have not added the modules into Bec.lib for official release.

The Files inside Moudules must be placed into Bec.lib
This means you need to extract current Bec.lib and add in the files & Directory from Modules to it. Then Repack it.

You will have to use the PackLib tool to do this.

Note. Do not put the "Modules" directory into Bec.lib Only the content inside it.
only this.

wx (dir)
new.py (file)
*.dll  (files)

After you added the file to your Bec.lib, you can delete the Modules directory from the "Plugins/Gui" directory.

Note. the full WX module is not included. 