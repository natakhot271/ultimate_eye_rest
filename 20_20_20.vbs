Set WshShell = CreateObject("WScript.Shell")
'   1st arg: the full python command in quotes
'   2nd arg: window style = 7 (minimize no activate)
'   3rd arg: True → wait for python.exe to exit before continuing
WshShell.Run """C:\Python312\python.exe"" ""C:\Users\natal\Documents\ultimate_eye_rest\20_20_20.py""", 7, True