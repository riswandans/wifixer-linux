#!/usr/bin/python
import os
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
os.system("TYPE=$(lspci -nnk | grep -A3 0280 | grep driver); echo $TYPE")

driver = raw_input(color + "Wifi driver name: " + default)
validation = raw_input(color + "Are you sure want to fix your wifi? (y/n) " + default)
if validation == "y":
	os.system("sudo modprobe -r " + driver)
	os.remove("/etc/modprobe.d/" + driver + ".conf")
	file = os.open("/etc/modprobe.d/" + driver + ".conf",os.O_RDWR|os.CREAT)
	write = os.write(file,"options " + driver + " fwlps=N ips=N")
	os.close(file)
	os.system('notify-send "WiFi Connection" "Success Installed driver ' + driver + '" -i notification-network-wireless-connected')
	print "Reboot your computer"
else:
	exit
