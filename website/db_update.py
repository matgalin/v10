from flask import jsonify, json
import psycopg2
import time
import os
from datetime import datetime
import password as password
login=password.db
#### UPDATE	

###Update CM COnfiguration	
def CM_configuration(id, name, description):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""UPDATE cm_configuration SET name = '%s', description = '%s' WHERE id= '%s'""" % (name, description, id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	
###NEW CCAP########################################################################	
def CCAP_configuration_new(id, name, description, type):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""UPDATE ccap_configuration_new SET name = '%s', description = '%s', type='%s' WHERE id= '%s'""" % (name, description, type, id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
###Update Provisioning ipv4	
def PROV_ipv4(configuration_id, routers, time, tftp, pool_range, subnet):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""UPDATE prov_ipv4 SET routers = '%s', time = '%s', tftp = '%s', pool_range = '%s', subnet = '%s' WHERE configuration_id='%s'""" % (routers, time, tftp, pool_range, subnet, configuration_id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
###Update Provisioning ipv6	
def PROV_ipv6(configuration_id, routers, time, tftp, pool_range, subnet):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""UPDATE prov_ipv6 SET routers = '%s', time = '%s', tftp = '%s', pool_range = '%s', subnet = '%s' WHERE configuration_id= '%s'""" % (routers, time, tftp, pool_range, subnet, configuration_id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
###Update Provisioning configuration
def PROV_configuration(configuration_id, configuration_name_main, configuration_description_main, configuration_ip_main, configuration_default_cm_configuration_id, configuration_tftp_directory, configuration_dhcp_directory, configuration_dhcp_interface, configuration_dhcp_ip):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""UPDATE prov_configuration SET name = '%s', description = '%s', ip_version = '%s', default_cm_configuration_id = '%s', tftp_directory = '%s', dhcp_directory = '%s', dhcp_interface = '%s', dhcp_ip = '%s'  WHERE id= '%s'""" % (configuration_name_main, configuration_description_main, configuration_ip_main, configuration_default_cm_configuration_id, configuration_tftp_directory, configuration_dhcp_directory, configuration_dhcp_interface, configuration_dhcp_ip, configuration_id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
###Update CCAP configuration
def CCAP_configuration(configuration_id, configuration_name_main, configuration_description_main, linear_card_main, bundle_main, fiber_node_main, max_ofdm_spectrum_ds_main, max_carrier_ds_main, base_channel_power_ds_main, ip_init_main):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""UPDATE ccap_configuration SET name = '%s', description = '%s', linear_card = '%s', bundle = '%s', fiber_node = '%s',  max_ofdm_spectrum_ds = '%s', max_carrier_ds = '%s', base_channel_power_ds = '%s', ip_init = '%s' WHERE id= '%s'""" % (configuration_name_main, configuration_description_main, linear_card_main, bundle_main, fiber_node_main, max_ofdm_spectrum_ds_main, max_carrier_ds_main, base_channel_power_ds_main, ip_init_main, configuration_id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
###Update TEST configuration
def TEST_configuration(configuration_id, name, description, prov_ip, prov_login, prov_password, prov_sudo, ccap_ip, ccap_login, ccap_password, ccap_sudo, logs_ip, logs_login, logs_password, logs_sudo, ccap_configuration_id, prov_configuration_id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""UPDATE test_configuration SET name = '%s', description = '%s', prov_ip = '%s', prov_login = '%s', prov_password = '%s', prov_sudo = '%s',  ccap_ip = '%s', ccap_login = '%s', ccap_password = '%s', ccap_sudo = '%s', logs_ip = '%s', logs_login = '%s', logs_password = '%s', logs_sudo = '%s', ccap_configuration_id='%s', prov_configuration_id='%s' WHERE id= '%s'""" % (name, description, prov_ip, prov_login, prov_password, prov_sudo, ccap_ip, ccap_login, ccap_password, ccap_sudo, logs_ip, logs_login, logs_password, logs_sudo, ccap_configuration_id, prov_configuration_id, configuration_id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
def TEST_history(id, type, value):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	if type=='change_status':
		sql="""UPDATE test_history SET is_running='%s', data_start=DEFAULT, data_end=DEFAULT, interval=DEFAULT, zabbix_group_id=DEFAULT, grafana_dashboard_uid=DEFAULT, data_planned_end=DEFAULT  WHERE id='%s'""" % (value, id)
	if type=='start':
		sql="""UPDATE test_history SET data_start='%s', is_running=1, data_end='', interval='' WHERE id='%s'""" % (value, id)
	if type=='stop':
		sql="""UPDATE test_history SET data_end='%s', is_running=2 WHERE id='%s'""" % (value, id)
	if type=='planned_end':
		sql="""UPDATE test_history SET data_planned_end='%s' WHERE id='%s'""" % (value, id)
	if type=='interval':
		sql="""UPDATE test_history SET interval='%s' WHERE id='%s'""" % (value, id)
	if type=='zabbix':
		sql="""UPDATE test_history SET zabbix_group_id='%s' WHERE id='%s'""" % (value, id)
	if type=='grafana':
		sql="""UPDATE test_history SET grafana_dashboard_uid='%s' WHERE id='%s'""" % (value, id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()