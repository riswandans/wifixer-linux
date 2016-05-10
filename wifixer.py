#!/usr/bin/env python2
import os
import os.path
import sys

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')
    
def check_file(name):
	return os.path.exists(name)
	
def check_os():
	if check_file("/etc/arch-release") == True:
		return "arch"
	elif check_file("/etc/lsb-release") == True:
		return "ubuntu"
	else:
		return 0

def install(driver):
	os.system("sudo modprobe -r " + driver)
	if check_file("/etc/modprobe.d/" + driver + ".conf") == True:
		os.remove("/etc/modprobe.d/" + driver + ".conf")
	file = open("/etc/modprobe.d/" + driver + ".conf", "w")
	file.write("options " + driver + " fwlps=N ips=N")
	file.close()
	os.system("sudo modprobe -i " + driver)

def notify(driver):
	if check_os() == "ubuntu":
		os.system('notify-send "WiFi Connection" "Success Installed driver ' + driver + '" -i notification-network-wireless-connected')

def application(driver, validation):
	if validation == "y":
		install(driver)
		notify(driver)
		print "Reboot your computer"
	else:
		exit
	
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
if check_os() == "ubuntu":
	os.system("TYPE=$(lspci -nnk | grep -A3 0280 | grep driver); echo $TYPE")
elif check_os() == "arch":
	os.system("lspci | grep 'Network'")

driver = raw_input(color + "Wifi driver name: " + default)
validation = raw_input(color + "Are you sure want to fix your wifi? (y/n) " + default)
application(driver,validation)
