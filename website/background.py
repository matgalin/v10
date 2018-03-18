import time
import json
import prepare_files_main as main_files
import prepare_files_ccap_new as ccap_files_new	##prepare files for ccap
import prepare_files_prov as prov_files
import prepare_files_cm as cm_files ##prepare files for cm
import monit_zabbix as zabbix ##prepare monitoring tools
import monit_grafana as grafana
import ansible as ansible
import db_get as db_get
import test_history as test_history
import test_logs as test_logs
import startup as startup
import generate_report as generate

global configuration_status
configuration_status = []
def start_configuration(id, interval):
	global configuration_status
	##main status
	TEST_history=db_get.TEST_history(id)
	TEST_configuration=db_get.TEST_configuration(TEST_history[0]['configuration_id'])
	TEST_configuration[0]['name']=TEST_configuration[0]['name']+'_'+TEST_history[0]['name']
	###set test configuration flag to "configuring"
	test_history.start_prepare(TEST_history)
	###add configuring data to main array
	status_temp={"configuration_id": TEST_configuration[0]['id'], "history_id": id, "status": 1, "content": []}
	print status_temp
	configuration_status.append(status_temp)
	time.sleep(2)
	###report that configuration started
	report_status('Executing Configuration', 'Start', 2)
	time.sleep(2)
	##prepare hosts data
	
	############################################################################ ANSIBLE HOST FILE
	if configuration_status[0]['status']!=2:
		report_status('Host file', 'Start', 2)
		main_files.prepareHosts(TEST_configuration)	
		time.sleep(2)
	############################################################################ KEA PROV FILE
	if configuration_status[0]['status']!=2:
		report_status('Host file', 'OK', 0)
		time.sleep(2)
		##prepare provisioning data
		report_status('Prov file', 'Start', 2)
		cable_modems_ip=prov_files.preparePROVmain(TEST_configuration)
	############################################################################ CM CFG FILE
	if configuration_status[0]['status']!=2:
		report_status('Prov file', 'OK', 0)
		time.sleep(2)
		report_status('CM files', 'Start', 2)
		cm_files.createCMconfig(TEST_configuration)
	############################################################################ ZABBIX
	if configuration_status[0]['status']!=2:
		report_status('CM files', 'OK', 0)
		time.sleep(2)
		#prepare Zabbix configuration
		report_status('Zabbix', 'Start', 2)
		zabbix_group_id=zabbix.run(TEST_configuration, cable_modems_ip)
	############################################################################ GRAFANA
	if configuration_status[0]['status']!=2:
		report_status('Zabbix', 'OK', 0)
		time.sleep(2)
		###prepare Grafana configureation
		report_status('Grafana', 'Start', 2)
		grafana_dashboard_uid=grafana.run(TEST_configuration)
		time.sleep(2)
		#configuration_status[0]['status']=2
	############################################################################ ANSIBLE TASKS
	if configuration_status[0]['status']!=2:
		report_status('Grafana', 'OK', 0)
		time.sleep(2)
		report_status('Ansible', 'Start', 2)
		ansible.run_tasks(TEST_configuration)
		time.sleep(2)
	############################################################################ CCAP CFG
	if configuration_status[0]['status']!=2:
	
		report_status('Ansible', 'OK', 0)
		time.sleep(2)
		report_status('CCAP Clear', 'Start', 2)
		ccap_files_new.clearCCAPconf(TEST_configuration)
	
	
	if configuration_status[0]['status']!=2:
		time.sleep(2)
		report_status('CCAP Clear', 'OK', 0)
		time.sleep(2)
		report_status('CCAP', 'Start', 2)
		ccap_files_new.createCCAPfiles(TEST_configuration)
		ccap_files_new.clearCM(TEST_configuration)
	#print json.dumps(configuration_status[0], indent=4, sort_keys=True)	
	if configuration_status[0]['status']!=2:
		report_status('CCAP', 'OK', 0)
		time.sleep(2)
		report_status('Enabling DHCP', 'Start', 2)
		ansible.enable_kea(TEST_configuration)
	if configuration_status[0]['status']!=2:
		report_status('DHCP', 'OK', 0)
		time.sleep(2)
		report_status('Executing Configuration', 'OK', 0)
		configuration_status[0]['status']=3
		test_history.start(TEST_history, zabbix_group_id, grafana_dashboard_uid, interval)
	if configuration_status[0]['status']==2:
		test_logs.insert_log(TEST_history, configuration_status[0]['content'][-1]['name'], configuration_status[0]['content'][-1]['status'])
		test_history.error(TEST_history)
		time.sleep(2)
	configuration_status = []		
	
	
def stop_test(id):
	TEST_history=db_get.TEST_history(id)
	TEST_configuration=db_get.TEST_configuration(TEST_history[0]['configuration_id'])
	TEST_configuration[0]['name']=TEST_configuration[0]['name']+'_'+TEST_history[0]['name']
	test_history.stop(TEST_history)
	zabbix.disable_hosts(TEST_configuration, TEST_history)
	#generate_report.generate(TEST_configuration)
	ansible.stop_tasks(TEST_configuration)
def startup_monitoring():
	while True:
		time.sleep(0.5)
		startup.look_for_finished_tests()
def report_status(name, status, flag):
	global configuration_status
	content={"id": len(configuration_status[0]['content']), "name": name, "status": status, "flag": flag}
	configuration_status[0]['content'].append(content)
	if flag==1:
		history_id=configuration_status[0]['history_id']
		TEST_history=db_get.TEST_history(history_id)
		test_history.error(TEST_history)
