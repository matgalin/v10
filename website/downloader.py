import json
import urllib2
import password as passwords
import csv
from datetime import datetime
##login to authenticate
##password to authenticate
## monitoring ip address
#######Zabbix request form (JSON)

def request(data):
	global address
	req = urllib2.Request('http://'+address+'/zabbix/api_jsonrpc.php')
	req.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(req, json.dumps(data))
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
	#print response
	global auth
	auth=response['result']

def get_all_groups():
	data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
	"params": {
		"selectHosts": "extend",
		"real_hosts": True
		
	},
    "auth": auth,
    "id": 1
	}
	response=request(data)
	return response
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
	#print json.dumps(response, indent=4, sort_keys=True)
	return response
def full():	
	## full procedure, getting information from API and put new groups and hosts here
	###### Magic stuff
	global login
	global password
	global address
	login='Admin'
	password='zabbix'
	address='10.100.100.16'
	authenticate()
	response=get_all_groups()
	#print json.dumps(response, indent=4, sort_keys=True)	
	main_content=[]
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

	
	
	
	
###ask zabbix for item history
def get_history(item_id):
	data = {
    "jsonrpc": "2.0",
    "method": "history.get",
    "params": {
		"history": 0,
		"itemids": item_id,
		"sortfield": "clock",
		"sortorder": "ASC",
    },
    "auth": auth,
    "id": 1
}
		
	response=request(data)
	return response
##download files, asking zabbix
def download(host_name, item_name, item_id):
	global login
	global password
	global address
	##get global data
	login='Admin'
	password='zabbix'
	address='10.100.100.16'
	file_name=host_name+'_'+item_name+'.csv'
	authenticate()
	response=get_history(item_id)
	#make csv file
	with open('download/'+file_name, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['date', item_name])
		for data in response['result']:
			time=datetime.fromtimestamp(int(data['clock'])).strftime('%Y-%m-%d %H:%M:%S')
			value=data['value']
			spamwriter.writerow([time, value])