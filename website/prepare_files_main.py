import db_get as db_get
import os	
import background as background
###prepare directory to config files per test
def prepareHosts(TEST_configuration):
	configuration_table=background.configuration_status[0]
	PROV_configuration=db_get.PROV_configuration(TEST_configuration[0]['prov_configuration_id'])
	dir="Ansible/tests/"+TEST_configuration[0]['name']+"/configs"  ##create directory path
	##then create directory if doesnt exist
	try: 
		os.makedirs(dir)
	except OSError:
		if not os.path.isdir(dir):
			raise
			
	###content contains information about hosts
	hosts_content="""
[localhost]
127.0.0.1
[ccap]
"""+TEST_configuration[0]['ccap_ip']+"""
[ccap:vars]
ccap_user="""+TEST_configuration[0]['ccap_login']+"""
ccap_pass="""+TEST_configuration[0]['ccap_password']+"""
ccap_enable="""+TEST_configuration[0]['ccap_sudo']+"""
[server]
"""+TEST_configuration[0]['prov_ip']+"""
[server:vars]
ansible_ssh_user="""+TEST_configuration[0]['prov_login']+"""
ansible_ssh_pass="""+TEST_configuration[0]['prov_password']+"""
ansible_sudo_pass="""+TEST_configuration[0]['prov_sudo']+"""
dhcp="""+PROV_configuration[0]['dhcp_directory']+"""
tftp="""+PROV_configuration[0]['tftp_directory']
	###save content to file
	try:
		file_hosts = open("Ansible/tests/"+TEST_configuration[0]['name']+"/hosts", "wb")
	except:
		background.report_status('Creating Host File', 'Error', 1)
		background.configuration_status['status']=2
		return 0
	else:
		file_hosts.write(hosts_content)
		file_hosts.close()
		