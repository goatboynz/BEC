This tool is for repacking the Bec.lib

This is a console application.

If you want to add in or use extra 3rd party modules, then you need to extract the Bec.lib using PackLib.exe or 7zip.exe, but you can not use 7zip.exe to repack it.
Once extracted. you add in your wanted modules. and repact it again.

-------------------------------------------
To Extract a Lib Archive do the following.

1 * Copy : Bec.lib from "C:\Bec" into example: "C:\Bec\Tools"
2 * Run  : PackLib.exe -e Bec.lib

When you extract a Lib Archive, PackLib will create a directory in the current dir "cwd" with the same name as the Lib Archive without the .lib extension ofcource.
So in this case we will get it like this, "C:\Bec\Tools\Bec"


-------------------------------------------
To Create a Lib Archive do the following.

NOTE. USE THE FULL PATH WITH -s

1 * run : PackLib.exe -d "C:\Bec\Tools\Bec" -l Bec.lib

Will result in "C:\Bec\Tools\Bec.lib"

PackLib will create the Lib Archive file in the current directory "cwd". 

Now Copy the file in "C:\Bec\Tools\Bec.lib" back to "C:\Bec\Bec.lib"



-------------------------------------------
Do not delete the Python26.dll file,
