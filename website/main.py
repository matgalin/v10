from flask import Flask, redirect, Response, jsonify, session, render_template, request, send_from_directory, json
from flask_session import Session
import urllib
import psycopg2
import os
from threading import Thread
import time
import db_get as db_get  ## get data from database
import db_insert as db_insert ##insert data to database
import db_remove as db_remove ##remove data from dayanase
import db_update as db_update ##update data in database
import prepare_files_main as main_files
import prepare_files_ccap_new as ccap_files_new	##prepare files for ccap
import prepare_files_prov as prov_files
import prepare_files_cm as cm_files ##prepare files for cm
import ansible as ansible
import test_history as test_history
import downloader as downloader
import background as background
import monit_zabbix as zabbix ##prepare monitoring tools
import monit_grafana as grafana
import startup as startup
import ssh as ssh
import time_conversion as time_conversion
import generate_report as report
from datetime import date
from datetime import datetime
import ccap_data as ccap_data

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "Very, very, really very secret string."
########################################################################################################
#######################################################################################################
####################################################################################################### Background thread
########################################################################################################
#######################################################################################################	

startup.look_for_errors()
thread = Thread(target=background.startup_monitoring)
thread.daemon = True
thread.start()

########################################################################################################
#######################################################################################################
#######################################################################################################  main page
########################################################################################################
#######################################################################################################	
@app.route('/')	
@app.route('/index')	
def index():	
	return render_template('index.html')
########################################################################################################
#######################################################################################################
####################################################################################################### SHOW DATA (everything)
########################################################################################################
#######################################################################################################	
##### Cable Modem List	
@app.route('/TOOLS/CableModems')	
def CableModems():	
	CM_List=db_get.CM_List()
	PROV_cm=db_get.PROV_cm('all')
	PROV_configuration=db_get.PROV_configuration('all')
	return render_template('TOOLS/CableModems.html',
	CM_List=CM_List,
	PROV_cm=PROV_cm,
	PROV_configuration=PROV_configuration)
### Data downloader tool
@app.route('/TOOLS/DataDownloader')	
def DataDownloader():	
	downloader_data=downloader.full()
	return render_template('TOOLS/DataDownloader.html',
	downloader_data=downloader_data)
	
##### Cable Modem Config Files list
@app.route('/CM/data/')
def CMdata():	
	CM_configuration=db_get.CM_configuration('all')  ##get all config files
	return render_template('CM/data.html',
	CM_configuration=CM_configuration)	
	
##### Provisioning Data list
@app.route('/PROV/data/')
def PROVdata():	
	PROV_configuration=db_get.PROV_configuration('all') ## get all provisioning data
	return render_template('PROV/data.html', 
	PROV_configuration=PROV_configuration)	
##### Test Configuration List	
@app.route('/TEST/data/')
def TESTdata():	
	TEST_configuration=db_get.TEST_configuration('all') ## get all test data
	TEST_history=db_get.TEST_history('all')	
	return render_template('TEST/data.html', 
	TEST_configuration=TEST_configuration,
	TEST_history=TEST_history)

##### CCAP Data list new
@app.route('/CCAP_new/data/')
def CCAPdatanew():	
	CCAP_configuration=db_get.CCAP_configuration_new('all') ## get all CCAP data
	return render_template('CCAP_new/data.html', 
	CCAP_configuration=CCAP_configuration,
	ccap_data=ccap_data)	
########################################################################################################
#######################################################################################################
####################################################################################################### SHOW DATA specified by ID
########################################################################################################
#######################################################################################################	
####Show CCAP configuration
@app.route('/CCAP_new/file/<id>')
def CCAPfile(id):
	session['ccap_id_new'] = id  ## chosen cm file
	CCAP_part=db_get.CCAP_part() ## get all parts of config file
	CCAP_configuration_new=db_get.CCAP_configuration_new('all') ##get all config files
	This_CCAP_configuration=db_get.CCAP_configuration_new(id) ## get all data from specified config file 
	return render_template('CCAP_new/file.html', 
	CCAP_part=CCAP_part,
	This_CCAP_configuration=This_CCAP_configuration,
	CCAP_configuration_new=CCAP_configuration_new,
	ccap_data=ccap_data)	
##### CM File configuration	
@app.route('/CM/file/<id>')
def CMfile(id):
	session['cm_id'] = id  ## chosen cm file
	CM_part=db_get.CM_part() ## get all parts of config file
	CM_configuration=db_get.CM_configuration('all') ##get all config files
	This_CM_configuration=db_get.CM_configuration(id) ## get all data from specified config file 
	return render_template('CM/file.html', 
	CM_part=CM_part,
	This_CM_configuration=This_CM_configuration,
	CM_configuration=CM_configuration)	
##### Provisioning data configuration
@app.route('/PROV/conf/<id>')
def PROVconf(id):
	session['prov_id'] = id  ## chosen provisioning config
	PROV_configuration=db_get.PROV_configuration(id)  ##get provisioning data
	PROV_ipv4=db_get.PROV_ipv4(id)	##get provisioning data for ipv4
	PROV_ipv6=db_get.PROV_ipv6(id)	##get provisioning data for ipv6
	PROV_cm=db_get.PROV_cm(id)  ## get configs for specified cable modems
	CM_configuration=db_get.CM_configuration('all') #get all config files
	return render_template('PROV/conf.html', 
	PROV_configuration=PROV_configuration, 
	PROV_ipv4=PROV_ipv4,
	PROV_ipv6=PROV_ipv6,
	PROV_cm=PROV_cm,
	CM_configuration=CM_configuration)
	
#### Test scenario configuration	
@app.route('/TEST/conf/<id>')
def TESTconf(id):
	session['test_id'] = id ##chosen test config
	TEST_configuration=db_get.TEST_configuration(id) ##get test config configuration data by ID
	CCAP_configuration=db_get.CCAP_configuration_new('all')	##get all CCAP configurations
	PROV_configuration=db_get.PROV_configuration('all')  ##get all PROV configurations
	return render_template('TEST/conf.html', 
	TEST_configuration=TEST_configuration, 
	CCAP_configuration=CCAP_configuration,
	PROV_configuration=PROV_configuration)		

#### Test Control Panel
@app.route('/TEST/control/<id>')
def TESTcontrol(id):
	zabbix_data=[]
	add_1=None
	add_2=None
	session['history_id'] = id ##chosen test config
	TEST_history=db_get.TEST_history(id) ##get test config history data by ID
	TEST_configuration=db_get.TEST_configuration(TEST_history[0]['configuration_id']) ##get test config configuration data by ID
	try:
		TEST_logs=db_get.TEST_logs(id) ##get logs/error data by ID
	except: 
		TEST_logs=[]
		pass
	#print json.dumps(TEST_history, indent=4, sort_keys=True)
	if TEST_history[0]['is_running'] == 1:
		add_1=time_conversion.date_to_unix(TEST_history[0]['data_start'])
		zabbix_data=zabbix.get_data(TEST_configuration, TEST_history)
		add_1=add_1*1000
	elif TEST_history[0]['is_running'] == 2:
		add_1=time_conversion.date_to_unix(TEST_history[0]['data_start'])
		add_1=add_1*1000
		add_2=time_conversion.date_to_unix(TEST_history[0]['data_end'])
		add_2=add_2*1000
		zabbix_data=zabbix.get_data(TEST_configuration, TEST_history)
	return render_template('TEST/control.html', 
	TEST_configuration=TEST_configuration,
	TEST_history=TEST_history,
	TEST_logs=TEST_logs,
	zabbix_data=zabbix_data,
	add_1=add_1,
	add_2=add_2)	
	
########################################################################################################
#######################################################################################################
####################################################################################################### UPDATE DATA
########################################################################################################
#######################################################################################################	
@app.route('/update/<type>', methods=['POST'])
def update(type):
	####################################################################################################### UPDATE PROV
	if type=='PROVconf':
		prov_id=session['prov_id']## chosen provisioning config
		idList=request.form['mainIds']  ## get List of updated elements
		if idList != '': 
			idList=idList.split(',')
			db_remove.PROV_cm(prov_id)  ### Remove configs for specified provisioning config
			for id in idList:
				###get all elements posted in HTML page
				cableModems=request.form['cable_modems_'+id[5:]] ##[5:] becouse remove first letters of HTML identifier
				ip4=request.form['ip4_'+id[5:]]
				ip6=request.form['ip6_'+id[5:]]
				routers4=request.form['routers4_'+id[5:]]
				routers6=request.form['routers6_'+id[5:]]
				configuration_file=request.form['configuration_file_'+id[5:]]
				####Insert new configs for specified provisioning config
				db_insert.PROV_cm(prov_id, 
				cableModems, 
				ip4, 
				ip6,
				routers4,
				routers6,
				configuration_file)	
		###get all elements posted in HTML page
		configuration_name_main=request.form['configuration_name_main']
		configuration_description_main=request.form['configuration_description_main']
		configuration_ip_main=request.form['configuration_ip_main']
		configuration_default_cm_configuration_id_main=request.form['configuration_default_cm_configuration_id_main']
		configuration_tftp_directory_main=request.form['configuration_tftp_directory_main']
		configuration_dhcp_directory_main=request.form['configuration_dhcp_directory_main']
		configuration_dhcp_interface_main=request.form['configuration_dhcp_interface_main']
		configuration_dhcp_ip_main=request.form['configuration_dhcp_ip_main']
		###get all elements posted in HTML page for IPv4
		if configuration_ip_main=='IPv4' or configuration_ip_main=='IPv4 and IPv6':
			routers=request.form['routers']
			time=request.form['time']
			tftp=request.form['tftp']
			pool_range=request.form['pool_range']
			subnet=request.form['subnet']
			
			###Update IPv4 informations
			db_update.PROV_ipv4(prov_id, routers, time, tftp, pool_range, subnet)
		###get all elements posted in HTML page for IPv6	
		if configuration_ip_main=='IPv6' or configuration_ip_main=='IPv4 and IPv6':
			routers=request.form['routers6']
			time=request.form['time6']
			tftp=request.form['tftp6']
			pool_range=request.form['pool_range6']
			subnet=request.form['subnet6']
		
			###Update IPv6 informations
			db_update.PROV_ipv6(prov_id, routers, time, tftp, pool_range, subnet)
		###Update Main informations
		db_update.PROV_configuration(prov_id,
		configuration_name_main,
		configuration_description_main,
		configuration_ip_main,
		configuration_default_cm_configuration_id_main,
		configuration_tftp_directory_main,
		configuration_dhcp_directory_main,
		configuration_dhcp_interface_main,
		configuration_dhcp_ip_main)
		return redirect('/PROV/conf/'+session['prov_id'])
	####################################################################################################### UPDATE CM FILE
	if type=='CMfile': 
		cm_id=session['cm_id'] ##chosen config file
		idList=request.form['mainIds'] ##get List of updated elements
		idList=idList.split(',')
		order_nr=0;
		db_remove.CM_part(cm_id) ##remove old parts of config file
		if idList!='':
			for id in idList:
				###get all elements posted in HTML page
				partContent=request.form[id]
				partName=request.form[id+'_name']
				db_insert.CM_part(cm_id, 
				partName, 
				partContent, 
				order_nr)
				order_nr+=1
		groupName=request.form['group_name']
		groupDescription=request.form['group_description']
		###Update Config File
		db_update.CM_configuration(cm_id,
		groupName,
		groupDescription)
		return redirect('/CM/file/'+session['cm_id'])
	####################################################################################################### UPDATE CCAP CONF
	if type=='CCAPfile': 
		ccap_id_new=session['ccap_id_new'] ##chosen config file
		idList=request.form['mainIds'] ##get List of updated elements
		idList=idList.split(',')
		order_nr=0;
		db_remove.CCAP_part(ccap_id_new) ##remove old parts of config file
		if idList!='':
			for id in idList:
				###get all elements posted in HTML page
				partContent=request.form[id]
				partName=request.form[id+'_name']
				partNr=request.form[id+'_nr']
				db_insert.CCAP_part(ccap_id_new, 
				partName, 
				partContent, 
				order_nr,
				partNr)
				order_nr+=1
		CCAPname=request.form['ccap_name']
		CCAPdescription=request.form['ccap_description']
		CCAPtype=request.form['ccap_type']
		###Update Config File
		db_update.CCAP_configuration_new(ccap_id_new,
		CCAPname,
		CCAPdescription,
		CCAPtype)
		return redirect('/CCAP_new/file/'+session['ccap_id_new'])
		
		
	####################################################################################################### UPDATE TEST SCENARIO
	if type=='TESTconf':
		test_id=session['test_id'] ## chosen Test Configuration config
		###get all elements posted in HTML page
		configuration_name=request.form['configuration_name']
		configuration_description=request.form['configuration_description']
		ccap_configuration_id=request.form['ccap_configuration_id']
		prov_configuration_id=request.form['prov_configuration_id']
		
		prov_ip=request.form['prov_ip']
		prov_login=request.form['prov_login']
		prov_password=request.form['prov_password']
		prov_sudo=request.form['prov_sudo']
		
		ccap_ip=request.form['ccap_ip']
		ccap_login=request.form['ccap_login']
		ccap_password=request.form['ccap_password']
		ccap_sudo=request.form['ccap_sudo']
		
		logs_ip=request.form['logs_ip']
		logs_login=request.form['logs_login']
		logs_password=request.form['logs_password']
		logs_sudo=request.form['logs_sudo']
		##update test configuration
		db_update.TEST_configuration(test_id,
		configuration_name,
		configuration_description,
		prov_ip,
		prov_login,
		prov_password,
		prov_sudo,
		ccap_ip,
		ccap_login,
		ccap_password,
		ccap_sudo,
		logs_ip,
		logs_login,
		logs_password,
		logs_sudo,
		ccap_configuration_id,
		prov_configuration_id)
		return redirect('/TEST/conf/'+session['test_id'])
			
	
########################################################################################################
#######################################################################################################
####################################################################################################### INSERT DATA
########################################################################################################
#######################################################################################################	
@app.route('/insert/<type>', methods=['POST'])
def insert(type):
	####################################################################################################### insert prov config
	if type=='PROVconf':
		try:
			name=request.form['test_configuration']
		except:
			pass
		else:
			description=request.form['test_description']
			db_insert.PROV_configuration(name, description)  ## insert name and description to database
		return redirect('/PROV/data/')
	####################################################################################################### insert cm config
	if type=='CMfile':
		try:
			name=request.form['group_configuration']
		except:
			pass
		else:
			description=request.form['group_description']	
			db_insert.CM_configuration(name, description)			## insert name and description to database
		return redirect('/CM/data/')
	####################################################################################################### insert ccap configuration file
	if type=='CCAPfile':
		try:
			name=request.form['ccap_configuration']
		except:
			pass
		else:
			description=request.form['ccap_description']
			type=request.form['ccap_type']			
			db_insert.CCAP_configuration_new(name, description, type)			## insert name and description to database
		return redirect('/CCAP_new/data/')
	####################################################################################################### insert test scenario
	if type=='TESTconf':
		try:
			name=request.form['test_configuration']
		except:
			pass
		else:	
			db_insert.TEST_configuration(name, ' ')	## insert name and description to database
		idList=request.form['mainIds'] ##get List of updated elements
		now=time_conversion.date_to_readable(time_conversion.now_date())
		if idList != '': 
			idList=idList.split(',')
			for id in idList:
				id=id[12:]
				###get all elements posted in HTML page
				history_name=request.form['history_name_'+id] 
				history_description=request.form['history_description_'+id]
				db_insert.TEST_history(id, 
				history_name, 
				history_description, 
				now)
		return redirect('/TEST/data/')
########################################################################################################
#######################################################################################################
####################################################################################################### DELETE DATA
########################################################################################################
#######################################################################################################		
@app.route('/delete/<type>/<id>', methods=['POST'])
def delete(type, id):
	####################################################################################################### delete prov conf
	if type=='PROVdata':
		db_remove.PROV_configuration(id)
		return redirect('/PROV/data/')
		####################################################################################################### delete prov cm conf
	if type=='PROVconf':
		db_remove.PROV_cm_single(id)
		return redirect('/PROV/conf/'+session['prov_id'])	
		####################################################################################################### delete cm file
	if type=='CMfile':
		db_remove.CM_configuration(id)
		return redirect('/CM/data/')
		####################################################################################################### delete ccap conf
	if type=='CCAPfile':
		db_remove.CCAP_configuration_new(id)
		return redirect('/CCAP_new/data/')
		####################################################################################################### delete test scenario
	if type=='TESTdata':
		db_remove.TEST_configuration(id)
		return redirect('/TEST/data/')		
########################################################################################################
#######################################################################################################
####################################################################################################### download file
########################################################################################################
#######################################################################################################		
@app.route('/download/<type>/<host_name>/<item_name>/<item_id>')	
def download(type, host_name, item_name, item_id):
	file_name=host_name+'_'+item_name+'.csv'
	if type=='test_status':
		id=session['test_id']
		TEST_configuration=db_get.TEST_configuration(id)
		TEST_history=db_get.TEST_history(id)
		zabbix.download(TEST_configuration, TEST_history, host_name, item_name, item_id)
	if type=='data_downloader':
		downloader.download(host_name, item_name, item_id)	
	return send_from_directory('download', file_name, as_attachment=True, attachment_filename=host_name+'_'+item_name+'.csv')
	
	

########################################################################################################
#######################################################################################################
####################################################################################################### TODO/ to finish
########################################################################################################
#######################################################################################################			
@app.route('/deletelog/')	
def test():	
	db_remove.delete_log()
		
	return render_template('test2.html')
	
@app.route('/cleartest/<id>')	
def cleartest(id):	
	db_update.TEST_history(id, 'change_status', 0)
	return redirect('/TEST/control/'+id)

@app.route('/report/<id>')	
def report_create(id):	
	TEST_history=db_get.TEST_history(id)
	TEST_configuration=db_get.TEST_configuration(TEST_history[0]['id'])
	name=report.create(TEST_configuration, TEST_history)
	return send_from_directory('download/reports', name, as_attachment=True, attachment_filename=name)

########################################################################################################
#######################################################################################################
####################################################################################################### JSON response during test execution
########################################################################################################
#######################################################################################################		
@app.route('/run_test_scenario/<type>/<id>/<additional>', methods=['POST'])
def run_test_scenario(type, id, additional):
	if type=='start':
		if len(background.configuration_status)==0:
			#CCAP_configuration_new=db_get.CCAP_configuration_new(id)
			thread = Thread(target=background.start_configuration, args=(id,), kwargs={'interval':additional})
			thread.daemon = True
			thread.start()
			return json.dumps({"status": 1, "msg": "ok"});
		else:
			return json.dumps({"status": 0, "msg": "other is running"});
	if type=='get':
		if len(background.configuration_status)!=0:
			if background.configuration_status[0]['history_id']==id:
				#print background.configuration_status[0]
				return json.dumps({"status": 1, "msg": "ok", "response": background.configuration_status[0]});
			else:
				return json.dumps({"status": 0, "msg": "u cant get other test"});
		else:
			return json.dumps({"status": 0, "msg": "something is wrong"});
	if type=='stop':
		TEST_history=db_get.TEST_history(id)
		if TEST_history[0]['is_running']==1:
			
			thread = Thread(target=background.stop_test, args=(id,))
			thread.daemon = True
			thread.start()
			return json.dumps({"status": 1, "msg": "ok"});
		else:
			return json.dumps({"status": 0, "msg": "nonono"});
	
		
		
	
########################################################################################################
#######################################################################################################
####################################################################################################### start website
########################################################################################################
#######################################################################################################			
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)  ## host ip and port
	
	
	

	



