import json
import urllib2
import password as passwords
import csv
import background as background
from datetime import datetime
import db_get as db_get
##login to authenticate
##password to authenticate
## monitoring ip address
#######Zabbix request form (JSON)
def request(data):
	global address
	req = urllib2.Request('http://'+address+'/zabbix/api_jsonrpc.php')
	req.add_header('Content-Type', 'application/json')
	try:
		response = urllib2.urlopen(req, json.dumps(data))
	except:
		background.configuration_status[0]['status']=2
		background.report_status('Zabbix Connection', 'Connection error, check IP settings', 1)
		return 0
	else:
		response=json.load(response)
		return response
#######Authentication, gettining api key
def authenticate():
	global login
	global password
	data ={
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": login,
        "password": password
    },
    "id": 1,
	}
	response=request(data);
	if response==0:
		return 0
	#print response
	global auth
	try:
		auth=response['result']
	except:
		auth=response['error']['data']
		background.configuration_status[0]['status']=2
		background.report_status('Zabbix Authentication', auth, 1)
	else:
		auth=response['result']
#######Creating new group for new test
def create_group(configuration_name):
	data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.create",
    "params": {
        "name": configuration_name
    },
    "auth": auth,
    "id": 1
	}
	response=request(data);
	return response.get('groupids')
####### If group exist(becouse of beta testing), get hosts from group	
def get_group(configuration_name):
	data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
	"params": {
		"filter": {
			"name": configuration_name
			},
		"selectHosts": "extend"
	},
    "auth": auth,
    "id": 1
	}
	response=request(data)
	return response
####### And delete them. Because this is still beta
def delete_hosts(host_id):
	data = {
    "jsonrpc": "2.0",
    "method": "host.delete",
	"params": [
        host_id

    ],
    "auth": auth,
    "id": 1
	}
	request(data);
## get template id of our template	
def get_template(template_id):
	data = {
    "jsonrpc": "2.0",
    "method": "template.get",
	"params": {
		"templateids": template_id,
		"output": "extend"
	},
    "auth": auth,
    "id": 1
	}
	response=request(data)
	try:
		variabe=response['result'][0]
	except:
		background.configuration_status[0]['status']=2
		background.report_status('Zabbix Get Default Template', 'Template ID doesnt exist', 1)
	else:	
		return 0
##create our host; 
def create_host(name, ip, group_id, template_id):
	data = {
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": name,
        "interfaces": [
            {
                "type": 2,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "161"
            }
        ],
        "groups": [
            {
                "groupid": group_id
            }
        ],
        "templates": [
            {
                "templateid": template_id
            }
        ]
    },
    "auth": auth,
    "id": 1
	}
	request(data);
	
## full procedure, getting information from API and put new groups and hosts here
def run(TEST_configuration, cable_modems_ip):
###### Magic stuff
	global login
	global password
	global address
	template_id=passwords.zabbix_template_id
	login=TEST_configuration[0]['logs_login']
	password=TEST_configuration[0]['logs_password']
	address=TEST_configuration[0]['logs_ip']
	name=TEST_configuration[0]['name']
	##using example template
	##authentication, get api key
	authenticate()
	if background.configuration_status[0]['status']==2:
		return 0
	else:
		group_id = create_group(name)
		if group_id is None:
			ids=get_group(name)
			group_id=ids['result'][0]['groupid']
			hosts=ids['result'][0]['hosts']
			for host in hosts:
				delete_hosts(host['hostid'])	
		get_template(template_id)
		if background.configuration_status[0]['status']==2:
			return 0
		else:
			for cable_modem in cable_modems_ip:
				host_ip=cable_modem['ip']
				host_name=host_ip+'_'+name
				create_host(host_name, host_ip, group_id, template_id)
			return group_id
	
#########################################################################################
#########################################################################################
#########################################################################################
##### data downloader per test
##get all hosts per group
def get_single_group(zabbix_group_id):
	data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
	"params": {
		"selectHosts": "extend",
		"groupids": zabbix_group_id
	},
    "auth": auth,
    "id": 1
	}
	response=request(data)
	return response
##get all items per specified host
def get_all_items(host_id):
	data = {
    "jsonrpc": "2.0",
    "method": "item.get",
    "params": {
        "hostids": host_id,
		"filter": { "state": "0" , "value_type": "0"}
		# "search": {
            # "value_type": "0"
        # }
    },
    "auth": auth,
    "id": 1
}
	response=request(data)
	return response	
	
##get data abourt specified group in json	
def get_data(TEST_configuration, TEST_history):
	global login
	global password
	global address
	##get global data
	login=TEST_configuration[0]['logs_login']
	password=TEST_configuration[0]['logs_password']
	address=TEST_configuration[0]['logs_ip']
	zabbix_group_id=TEST_history[0]['zabbix_group_id']
	authenticate()
	response=get_single_group(zabbix_group_id)
	main_content=[]
	##parsing json, creating new list with specified groups, hosts in and items in
	for group in response['result']:
		group_content={}
		group_content={"id": group['groupid'], "name": group['name'], "hosts":[]}
		main_content.append(group_content)
		#print json.dumps(group['name'], indent=4, sort_keys=True)
		for host in group['hosts']:
			host_content={}
			host_content={"id": host['hostid'], "name": host['name'], "items":[]}
			group_content['hosts'].append(host_content)
	for group in main_content:
		for host in group['hosts']:
			all_items=get_all_items(host['id'])
			for item in all_items['result']:
				item_content={}
				item_content={"id": item['itemid'], "name": item['name']}
				host['items'].append(item_content)
	return main_content
#########################################################################################
#########################################################################################
#########################################################################################
##### disable test=disable hosts
def set_status_1(hosts):
	data = {
    "jsonrpc": "2.0",
    "method": "host.massupdate",
	"params": {
		"hosts":[],
		"status": 1
	},
    "auth": auth,
    "id": 1
	}
	for host in hosts:
		host_list={"hostid": host['hostid']}
		data['params']['hosts'].append(host_list)
	response=request(data)
def disable_hosts(TEST_configuration, TEST_history):
	global login
	global password
	global address
	##get global data
	login=TEST_configuration[0]['logs_login']
	password=TEST_configuration[0]['logs_password']
	address=TEST_configuration[0]['logs_ip']
	zabbix_group_id=TEST_history[0]['zabbix_group_id']
	authenticate()
	response=get_single_group(zabbix_group_id)
	set_status_1(response['result'][0]['hosts'])
	
	
	
######################################################################
#####################################################################
##### data downloader: downloading data
###ask zabbix for item history
def get_history(item_id, time_from, time_till):
	data = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
		"history": 0,
		"itemids": item_id,
		"sortfield": "clock",
		"sortorder": "ASC",
		"time_from": time_from
    },
    "auth": auth,
    "id": 1
}
	if time_till != '':
		data['params'].update({"time_till": time_till})
		
	response=request(data)
	return response
##download files, asking zabbix
def download(TEST_configuration, TEST_history, host_name, item_name, item_id):
	global login
	global password
	global address
	##get global data
	login=TEST_configuration[0]['logs_login']
	password=TEST_configuration[0]['logs_password']
	address=TEST_configuration[0]['logs_ip']
	file_name=host_name+'_'+item_name+'.csv'
	time_from=TEST_history[0]['data_start']
	time_till=TEST_history[0]['data_end']
	##swap utc time to unix time
	time_from=int(datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S').strftime("%s"))
	if time_till != '':
		time_till=int(datetime.strptime(time_till, '%Y-%m-%d %H:%M:%S').strftime("%s"))
	authenticate()
	response=get_history(item_id, time_from, time_till)
	#make csv file
	with open('download/'+file_name, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['date', item_name])
		for data in response['result']:
			time=datetime.fromtimestamp(int(data['clock'])).strftime('%Y-%m-%d %H:%M:%S')
			value=data['value']
			spamwriter.writerow([time, value])
		
		

		
