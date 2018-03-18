from flask import jsonify, json
import psycopg2
import time
import os
from datetime import datetime
import password as password
login=password.db
#############################################CM DATA
#############################################################
## Get all information about cable modems
def CM_List():
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""SELECT id, vendor, mac, sn, nr FROM cm_list ORDER by id"""
	cur.execute(sql)
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "vendor": row[1], "mac": row[2], "sn": row[3], "nr": row[4]}
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()

## Get Information about Cable Modem configurations
def CM_configuration(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	if id=='all':
		sql="""SELECT id, name, description FROM cm_configuration ORDER by id ASC"""
	else:
		sql="""SELECT id, name, description FROM cm_configuration WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "name": row[1], "description": row[2]}
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()
	
## Get Information about all Parts of every Cable Modems
def CM_part():
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""SELECT id, configuration_id, name, content, order_nr FROM cm_part ORDER BY order_nr ASC"""
	cur.execute(sql)
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "configuration_id": row[1], "name": row[2], "content": row[3], "order_nr": row[4]}
		content['content']=content['content'].replace('\x07', ' ').replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace('"', '\\\"').replace('<', '\\\"').replace('>', '\\\"')
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()	

#####################Provisioning Data
#################################################
## Get Information about Provisioning configurations
def PROV_configuration(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	if id=='all':
		sql="""SELECT id, name, description, ip_version, default_cm_configuration_id, tftp_directory, dhcp_directory, dhcp_interface, dhcp_ip FROM prov_configuration ORDER by id ASC"""
	else:
		sql="""SELECT id, name, description, ip_version, default_cm_configuration_id, tftp_directory, dhcp_directory, dhcp_interface, dhcp_ip FROM prov_configuration WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "name": row[1], "description": row[2], "ip_version": row[3], "default_cm_configuration_id": row[4], "tftp_directory": row[5], "dhcp_directory": row[6], "dhcp_ip": row[8], "dhcp_interface": row[7]}
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()
	
	
	
### Get Information about Provisioning Configuration for IPv4	
def PROV_ipv4(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""SELECT id, routers, time, tftp, pool_range, subnet FROM prov_ipv4 WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "routers": row[1], "time": row[2], "tftp": row[3], "pool_range": row[4], "subnet": row[5]}
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()	
	
### Get Information about Provisioning Configuration for IPv6	
def PROV_ipv6(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""SELECT id, routers, time, tftp, pool_range, subnet FROM prov_ipv6 WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "routers": row[1], "time": row[2], "tftp": row[3], "pool_range": row[4], "subnet": row[5]}
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()	

### Get Information about specified Provisioning Configuration; small parts of config per cable modem
def PROV_cm(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	if id=='all':
		sql="""SELECT id, configuration_id, cm_configuration_id, ipv4, ipv6, routersv4, routersv6, cable_modem FROM prov_cm"""

	else:
		sql="""SELECT id, configuration_id, cm_configuration_id, ipv4, ipv6, routersv4, routersv6, cable_modem FROM prov_cm WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "configuration_id": row[1], "cm_configuration_id": row[2], "ipv4": row[3], "ipv6": row[4], "routersv4": row[5], "routersv6": row[6], "cable_modem": row[7]}
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()	
#####################################################################################################################	
#######################CCAP DATA new	


## Get Information about CCAP configurations
def CCAP_configuration_new(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	if id=='all':
		sql="""SELECT id, name, description, type FROM ccap_configuration_new ORDER by id ASC"""
	else:
		sql="""SELECT id, name, description, type FROM ccap_configuration_new WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "name": row[1], "description": row[2], "type": row[3]}
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()
	
	
## Get Information about all Parts of every Cable Modems
def CCAP_part():
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""SELECT id, configuration_id, name, content, order_nr, nr FROM ccap_part ORDER BY order_nr ASC"""
	cur.execute(sql)
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "configuration_id": row[1], "name": row[2], "content": row[3], "order_nr": row[4], "nr": row[5]}
		content['content']=content['content'].replace('\x07', ' ').replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace('"', '\\\"').replace('<', '\\\"').replace('>', '\\\"')
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()	


#####################TEST Data
#################################################
## Get Information about TEST configurations
def TEST_configuration(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	if id=='all':
		sql="""SELECT id, name, description, prov_ip, prov_login, prov_password, prov_sudo,  ccap_ip, ccap_login, ccap_password, ccap_sudo, logs_ip, logs_login, logs_password, logs_sudo,  ccap_configuration_id, prov_configuration_id FROM test_configuration"""
	else:
		sql="""SELECT id, name, description, prov_ip, prov_login, prov_password, prov_sudo,  ccap_ip, ccap_login, ccap_password, ccap_sudo, logs_ip, logs_login, logs_password, logs_sudo,  ccap_configuration_id, prov_configuration_id FROM test_configuration WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "name": row[1], "description": row[2], "prov_ip": row[3], "prov_login": row[4], "prov_password": row[5], "prov_sudo": row[6], "ccap_ip": row[7], "ccap_login": row[8], "ccap_password": row[9], "ccap_sudo": row[10], "logs_ip": row[11], "logs_login": row[12], "logs_password": row[13], "logs_sudo": row[14], "ccap_configuration_id": row[15], "prov_configuration_id": row[16]}
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()
	
def TEST_history(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	if id=='all':
		sql="""SELECT id, name, data_created, configuration_id, data_start, data_end, data_planned_end, interval, zabbix_group_id, is_running, grafana_dashboard_uid, configuration_id, description FROM test_history ORDER by id ASC"""
	else:
		sql="""SELECT id, name, data_created, configuration_id, data_start, data_end, data_planned_end, interval, zabbix_group_id, is_running, grafana_dashboard_uid, configuration_id, description FROM test_history WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "name": row[1], "data_created": row[2], "configuration_id": row[3], "data_start": row[4], "data_end": row[5], "data_planned_end": row[6], "interval": row[7], "zabbix_group_id": row[8], "is_running": row[9], "grafana_dashboard_uid": row[10], "configuration_id": row[11], "description": row[12]}
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()
def TEST_logs(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""SELECT id, name, content, date FROM test_logs WHERE history_id='%s' ORDER by id DESC""" % (id)
	cur.execute(sql)
	conn.commit()
	rows=cur.fetchall()
	payload= []
	content = {}
	for row in rows:
		content = {"id": row[0], "name": row[1], "content": row[2], "date": row[3]}
		
		content['content']=content['content'].replace('\x07', ' ').replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace('"', '\\\"').replace('<', '\\\"').replace('>', '\\\"')
		payload.append(content)
		content= {}
	return payload
	cur.close()
	conn.close()