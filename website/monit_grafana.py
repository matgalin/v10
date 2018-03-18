import json
import urllib2
import background as background
import password as password


def request(api_data, api_link, data):
	if api_data is None:
		req = urllib2.Request('http://'+address+'/grafana'+api_link+'')
	else:
		req = urllib2.Request('http://'+address+'/grafana'+api_link+''+api_data)
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', api_key)
	#try:
	try:
		if data is None:
			response = urllib2.urlopen(req)
		else:
			response = urllib2.urlopen(req, json.dumps(data))
	except:
		if api_link=='/api/dashboards/uid/':
			background.configuration_status[0]['status']=2
			background.report_status('Grafana Connection', 'Wrong default dashboard id', 1)
			#print 'Wrong Dashboard ID'
		if api_link=='/api/auth/keys':
			#print 'Wrong api key'
			background.configuration_status[0]['status']=2
			background.report_status('Grafana Connection', 'Wrong api key or ip data', 1)
		return 0
	else:
		response=json.load(response)
		return response

## request present and existing example data
def check_connection():
	api_link='/api/auth/keys'
	response=request(None, api_link, None)
	#print json.dumps(panels, indent=4, sort_keys=True)
def request_current_template(api_data):
	api_link='/api/dashboards/uid/'
	response=request(api_data, api_link, None)
	#print json.dumps(panels, indent=4, sort_keys=True)
	try:
		panels=response['dashboard']['panels']
	except: 
		return 0
	else:
		return panels

def create_new_template(name, panels):
	##creating data
	data = {
	  "dashboard": {
		"id": None,
		"title": name,
		"timezone": "browser",
		"panels": [],
		"version": 0
	  },
	  "overwrite": True
	}
	api_link='/api/dashboards/db'
	###make headers
	##iterating in example dashboard and changing group
	for panel in panels:
		for target in panel['targets']:
			target['group']['filter']= name
		data['dashboard']['panels'].append(panel)	
	
	response=request('', api_link, data)
	try: 
		response_uid=response['uid']
	except: 
		background.configuration_status[0]['status']=2
		background.report_status('Grafana', 'Dashboard failed', 1)
		return 0
	else:
		return response_uid
def run(TEST_configuration):	
	global api_key
	api_key=password.grafana_key
	global address
	
	api_data=password.grafana_dashboard_uid
	name=TEST_configuration[0]['name']
	address=TEST_configuration[0]['logs_ip']
	check_connection()
	if background.configuration_status[0]['status']==2:
		return 0
	panels=request_current_template(api_data)
	if background.configuration_status[0]['status']==2:
		return 0
	return create_new_template(name, panels)


	
		

