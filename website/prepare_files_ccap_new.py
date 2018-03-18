import db_get as db_get
import ssh as ssh
import background as background
import time
global cbr8_clear_list
cbr8_clear_list=[
{"name": "controller Upstream-Cable"},
{"name": "controller Integrated-Cable"},
{"name": "interface Cable"},
{"name": "interface Wideband-Cable"},
{"name": "cable Fiber-Node"}
]

###create config file for every specified Cable Modem
def createCCAPfiles(TEST_configuration):
	ccap_configuration_id=TEST_configuration[0]['ccap_configuration_id']
	HOST = TEST_configuration[0]['ccap_ip']
	USER = TEST_configuration[0]['ccap_login']
	PASSWORD = TEST_configuration[0]['ccap_password']
	SUDO = TEST_configuration[0]['ccap_sudo']
	#configuration_table=background.configuration_status[0]
	##CCAP Configuration Started
	flag = ssh.check_connection(HOST, USER, PASSWORD)
	###Check SSH Connection
	if flag==1:
		background.report_status('SSH Connection', 'wrong CCAP ip/login/password', '1')
		background.configuration_status[0]['status']=2
		return 0
	time.sleep(2)	
	##Check SUDO PASSWORD
	flag = ssh.check_sudo(HOST, USER, PASSWORD, SUDO)
	if flag==1:
		background.report_status('CCAP Authentication', 'wrong CCAP enable password', '1')
		background.configuration_status[0]['status']=2
		return 0
		
	time.sleep(2)
	##execute commands, line by line
	CCAP_part=db_get.CCAP_part()
	for parts in CCAP_part:
		if str(parts['configuration_id'])==str(ccap_configuration_id):
			name=parts['name']+' '+parts['nr']
			command=name+'\n'
			for line in parts['content'].splitlines():
				line=str(line).replace('\\r\\n', '\n').replace('\\"', '"')
				command+=line

			#execute commands
			command+="""
			"""
			flag = ssh.execute_command(HOST, USER, PASSWORD, SUDO, command, name)
			time.sleep(2)
			if flag==1:
				background.configuration_status[0]['status']=2
				return 0



############################################################
###########################################################CLEARING
def CBR8controllerUS(HOST, USER, PASSWORD, SUDO, name):
	list_of_defaults=[
	{"name": "channel-width"},
	{"name": "frequency"},
	{"name": "docsis-mode"},
	{"name": "modulation-profile"},
	]
	for us in range(0, 8):
		command=name+'\n'
		command+='us-channel '+str(us)+' shutdown\n'
		for default in list_of_defaults:
			command+='default us-channel '+str(us)+' '+default['name']+'\n'
		#print command
		ssh.clear_command(HOST, USER, PASSWORD, SUDO, command)


def CBR8controllerDS(HOST, USER, PASSWORD, SUDO, name):
	list_of_defaults=[
	{"name": "default max-carrier"},
	{"name": "no rf-chan 0 105"},
	{"name": "no rf-chan 158 162"},
	]
	command=name+'\n'
	for default in list_of_defaults:
		command+=default['name']+'\n'
	#print command
	ssh.clear_command(HOST, USER, PASSWORD, SUDO, command)

def CBR8default(HOST, USER, PASSWORD, SUDO, name):
	command='default '+name+'\n'
	ssh.clear_command(HOST, USER, PASSWORD, SUDO, command)

	
def clearCCAPconf(TEST_configuration):
	global cbr8_clear_list
	cbr8_fibernode=''
	cbr8_controllerUS=''
	cbr8_controllerDS=''
	cbr8_wideband=''
	cbr8_cable=''
	ccap_configuration_id=TEST_configuration[0]['ccap_configuration_id']
	HOST = TEST_configuration[0]['ccap_ip']
	USER = TEST_configuration[0]['ccap_login']
	PASSWORD = TEST_configuration[0]['ccap_password']
	SUDO = TEST_configuration[0]['ccap_sudo']
	CCAP_part=db_get.CCAP_part()
	flag = ssh.check_connection(HOST, USER, PASSWORD)
	if flag==1:
		background.report_status('SSH Connection', 'wrong CCAP ip/login/password', '1')
		background.configuration_status[0]['status']=2
		return 0
	time.sleep(2)	
	##Check SUDO PASSWORD
	flag = ssh.check_sudo(HOST, USER, PASSWORD, SUDO)
	if flag==1:
		background.report_status('CCAP Authentication', 'wrong CCAP enable password', '1')
		background.configuration_status[0]['status']=2
		return 0
	for parts in CCAP_part:
		if str(parts['configuration_id'])==str(ccap_configuration_id):
					##clear US Controler
				if parts['name'].find('controller Upstream-Cable')>-1:
					cbr8_controllerUS=parts['name']+' '+parts['nr']
					#CBR8controllerUS(HOST, USER, PASSWORD, SUDO, parts['name'])
					##clear DS Controler
				if parts['name'].find('controller Integrated-Cable')>-1:
					cbr8_controllerDS=parts['name']+' '+parts['nr']
					#CBR8controllerDS(HOST, USER, PASSWORD, SUDO, parts['name'])
				if parts['name'].find('cable Fiber-Node')>-1:
					cbr8_fibernode=parts['name']+' '+parts['nr']
					#CBR8default(HOST, USER, PASSWORD, SUDO, parts['name'])
				if parts['name'].find('interface Wideband-Cable')>-1:
					cbr8_wideband=parts['name']+' '+parts['nr']
					#CBR8default(HOST, USER, PASSWORD, SUDO, parts['name'])
				if parts['name'].find('interface Cable')>-1:
					cbr8_cable=parts['name']+' '+parts['nr']
					#CBR8default(HOST, USER, PASSWORD, SUDO, parts['name'])
	CBR8controllerUS(HOST, USER, PASSWORD, SUDO, cbr8_controllerUS)
	CBR8controllerDS(HOST, USER, PASSWORD, SUDO, cbr8_controllerDS)
	CBR8default(HOST, USER, PASSWORD, SUDO, cbr8_fibernode)
	CBR8default(HOST, USER, PASSWORD, SUDO, cbr8_wideband)
	CBR8default(HOST, USER, PASSWORD, SUDO, cbr8_cable)

def clearCM(TEST_configuration):
	ccap_configuration_id=TEST_configuration[0]['ccap_configuration_id']
	HOST = TEST_configuration[0]['ccap_ip']
	USER = TEST_configuration[0]['ccap_login']
	PASSWORD = TEST_configuration[0]['ccap_password']
	SUDO = TEST_configuration[0]['ccap_sudo']
	CCAP_part=db_get.CCAP_part()
	for parts in CCAP_part:
		if str(parts['configuration_id'])==str(ccap_configuration_id):
				if parts['name'].find('interface Cable')>-1:
					command='clear cable modem Cable'+parts['nr']+' all reset'
					ssh.clear_CM_command(HOST, USER, PASSWORD, SUDO, command)