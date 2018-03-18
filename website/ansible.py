import os
import commands
import background
import time
## run Ansible scripts
	
def execute_ansible(task_name, description, name):
	pass
	status, output = commands.getstatusoutput('ansible-playbook Ansible/'+task_name+'_start.yml -i Ansible/tests/'+name+'/hosts --extra-vars "test='+name+'"')
	if task_name=='dhcp_disable':
		print 0
	else:
		if task_name=='dhcp_enable_0':
			if status==0:
				background.report_status(description, 'DHCP Server exists', 1)
				return 1
			else:
				return 0
		else:	
			if status!=0:
				background.report_status(description, 'error', 1)
				return 1
			else:
				background.report_status(description, 'OK', 0)
				return 0


	
def run_tasks(TEST_configuration):
	name=TEST_configuration[0]['name']
	task_list=[
	{'task_name': 'local_0', 'task_description': 'Prepare localhost files'},
	{'task_name': 'local_1', 'task_description': 'Creating cable modems files'},
	{'task_name': 'local_2', 'task_description': 'Creating DHCP Configuration'},
	{'task_name': 'check_0', 'task_description': 'Check Connection to Prov Server'},
	{'task_name': 'tftp_0', 'task_description': 'Prepare remote host files'},
	{'task_name': 'tftp_1', 'task_description': 'Copy Cable Modem files'},
	{'task_name': 'kea_0', 'task_description': 'Copy Kea configuration'},
	{'task_name': 'dhcp_enable_0', 'task_description': 'Check if Kea is disabled'}
	]
	
	for task in task_list:
		time.sleep(2)
		status=execute_ansible(task['task_name'], task['task_description'], name)
		if status==1:
			background.configuration_status[0]['status']=2
			return 0
def enable_kea(TEST_configuration):
	name=TEST_configuration[0]['name']
	task_list=[
	{'task_name': 'dhcp_enable_1', 'task_description': 'Enable Kea'},
	{'task_name': 'dhcp_enable_2', 'task_description': 'Check if Kea is enabled'}
	]	
	for task in task_list:
		time.sleep(2)
		status=execute_ansible(task['task_name'], task['task_description'], name)
		print task['task_name']
		if status==1:
			background.configuration_status[0]['status']=2
			return 0
def stop_tasks(TEST_configuration):
	name=TEST_configuration[0]['name']
	task_list=[
	{'task_name': 'dhcp_disable', 'task_description': 'Disable Kea'}
	]
	
	for task in task_list:
		time.sleep(2)
		execute_ansible(task['task_name'], task['task_description'], name)
		# if status==1:
			# background.configuration_status[0]['status']=2
			# return 0