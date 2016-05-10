#!/usr/bin/python
import os
import os.path
import sys

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')
    
color = '\033[91m'
default = '\033[92m'
print default + """\

 __          __  _    __   _                      
 \ \        / / (_)  / _| (_)                     
  \ \  /\  / /   _  | |_   _  __  __   ___   _ __ 
   \ \/  \/ /   | | |  _| | | \ \/ /  / _ \ | '__|
    \  /\  /    | | | |   | |  >  <  |  __/ | |   
     \/  \/     |_| |_|   |_| /_/\_\  \___| |_|   
                                                  
                                                  
"""
if os.path.exists("/etc/arch-release") != True:
	os.system("TYPE=$(lspci -nnk | grep -A3 0280 | grep driver); echo $TYPE")
else:
	os.system("lspci")

driver = raw_input(color + "Wifi driver name: " + default)
validation = raw_input(color + "Are you sure want to fix your wifi? (y/n) " + default)
if validation == "y":
	if os.path.exists("/etc/arch-release") != True:
		notify(driver)
	print "Reboot your computer"
else:
	exit

def install(driver):
	os.system("sudo modprobe -r " + driver)
	if os.path.exists("/etc/modprobe.d/" + driver + ".conf") == True:
		os.remove("/etc/modprobe.d/" + driver + ".conf")
	file = open("/etc/modprobe.d/" + driver + ".conf", "w")
	file.write("options " + driver + " fwlps=N ips=N")
	file.close()
	os.system("sudo modprobe -i " + driver)

def notify(driver):
	os.system('notify-send "WiFi Connection" "Success Installed driver ' + driver + '" -i notification-network-wireless-connected')
