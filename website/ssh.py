import sys
import time
#sys.stderr = open('/dev/null')       # Silence silly warnings from paramiko
import paramiko as pm
#sys.stderr = sys.__stderr__
import os
import background as background
global enable_works
global error_text
global error_text2
global error_text3
global error_text4
enable_works="#"
error_text="%"
error_text2= "not valid"
error_text3= "overlap"
error_text4= "invalid"
valid_text= "now changed"
class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return
def check_connection(HOST, USER, PASSWORD):
	##check if can log to ssh
	client = pm.SSHClient()
	client.set_missing_host_key_policy(AllowAllKeys())
	try:
		client.connect(HOST, username=USER, password=PASSWORD)
	except: 
		return 1
	else:
		client.close()
		return 0
def check_sudo(HOST, USER, PASSWORD, SUDO):
	##check if sudo password works
	#global enable
	global error_text
	client = pm.SSHClient()
	client.set_missing_host_key_policy(AllowAllKeys())
	client.connect(HOST, username=USER, password=PASSWORD)
	channel = client.invoke_shell()
	enable="""enable
"""+SUDO+"""
"""
	#print enable
	channel.send(enable)
	time.sleep(2)
	output=channel.recv(65535)
	#print output
	error=output.find(enable_works)
	client.close()
	if error==-1:
		return 1
	else:
		return 0
##execute every single command
def execute_command(HOST, USER, PASSWORD, SUDO, command, name):
	global error_text
	global error_text2
	global error_text3
	global error_text4
	global valid_text
	client = pm.SSHClient()
	client.set_missing_host_key_policy(AllowAllKeys())
	client.connect(HOST, username=USER, password=PASSWORD)
	channel = client.invoke_shell()
	enable="""enable
"""+SUDO+"""
configure t
"""
	channel.send(enable)
	nvm=channel.recv(6000)
	time.sleep(2)
	channel.send(command)
	time.sleep(10)
	output=channel.recv(6000)
	#print output
	error=output.find(error_text)
	error2=output.find(error_text2)
	error3=output.find(error_text3)
	error4=output.find(error_text4)
	valid=output.find(valid_text)
	client.close()
	if (error!=-1 and valid!=-1) or (error==-1 and error2==-1 and error3==-1 and error4==-1):
		return 0
	else:
		background.report_status('CCAP: '+name, output, '1')
		#print output
		return 1

def clear_command(HOST, USER, PASSWORD, SUDO, command):
	client = pm.SSHClient()
	client.set_missing_host_key_policy(AllowAllKeys())
	client.connect(HOST, username=USER, password=PASSWORD)
	channel = client.invoke_shell()
	enable="""enable
"""+SUDO+"""
configure t
"""
	channel.send(enable)
	nvm=channel.recv(1024)
	time.sleep(2)
	channel.send(command)
	time.sleep(2)
	output=channel.recv(6000)
	#print output
	client.close()
def clear_CM_command(HOST, USER, PASSWORD, SUDO, command):
	client = pm.SSHClient()
	client.set_missing_host_key_policy(AllowAllKeys())
	client.connect(HOST, username=USER, password=PASSWORD)
	channel = client.invoke_shell()
	enable="""enable
"""+SUDO+"""
"""
	channel.send(enable)
	nvm=channel.recv(1024)
	time.sleep(2)
	channel.send(command)
	time.sleep(2)
	output=channel.recv(6000)
	#print output
	client.close()
