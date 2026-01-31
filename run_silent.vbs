Set WshShell = CreateObject("WScript.Shell")
strPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))
' This launches the bat file in invisible mode (0)
WshShell.Run chr(34) & strPath & "start_pikachu.bat" & chr(34), 0
Set WshShell = Nothing