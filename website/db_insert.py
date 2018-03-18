from flask import jsonify, json
import psycopg2
import time
import os
from datetime import datetime
import password as password
import db_get as db_get
login=password.db

#### INSERT	
##new Provisioning Cable Modem config
def PROV_cm(id, cable_modems, ip4, ip6, routers4, routers6, group_id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO prov_cm (configuration_id, cable_modem, ipv4, ipv6, routersv4, routersv6, cm_configuration_id) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (id, cable_modems, ip4, ip6, routers4, routers6, group_id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
##new Provisioning config	
def PROV_configuration(name, description):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO prov_configuration (name, description) VALUES ('%s', '%s')""" % (name, description)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	PROV_configuration=db_get.PROV_configuration('all')
	configuration_id=PROV_configuration[-1]['id']
	PROV_ipv4(configuration_id)
	PROV_ipv6(configuration_id)
##new Provisioning config ipv4
def PROV_ipv4(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO prov_ipv4 (configuration_id) VALUES ('%s')""" % (id)
	cur.execute(sql)
	id=cur.lastrowid
	conn.commit()
	cur.close()
	conn.close()
##new Provisioning config ipv6
def PROV_ipv6(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO prov_ipv6 (configuration_id) VALUES ('%s')""" % (id)
	cur.execute(sql)
	id=cur.lastrowid
	conn.commit()
	cur.close()
	conn.close()	
##new CM configuration
def CM_configuration(name, description):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO cm_configuration (name, description) VALUES ('%s', '%s')""" % (name, description)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
##new CM part
def CM_part(partGroup, partName, partContent, order_nr):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO cm_part (configuration_id, name, content, order_nr) VALUES ('%s', '%s', '%s', '%s')""" % (partGroup, partName, partContent, order_nr)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
##CCAP CONFIGURATION new######################################################################
def CCAP_configuration_new(name, description, type):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO ccap_configuration_new (name, description, type) VALUES ('%s', '%s', '%s')""" % (name, description, type)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
##new CCAP part
def CCAP_part(partGroup, partName, partContent, order_nr, nr):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO ccap_part (configuration_id, name, content, order_nr, nr) VALUES ('%s', '%s', '%s', '%s', '%s')""" % (partGroup, partName, partContent, order_nr, nr)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
##new Test configuration	
def TEST_configuration(name, description):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO test_configuration (name, description) VALUES ('%s', '%s')""" % (name, description)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	#TEST_configuration=db_get.TEST_configuration('all')
	#configuration_id=TEST_configuration[-1]['id']
	#TEST_history(configuration_id)
	
def TEST_history(configuration_id, name, description, data_created):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO test_history (configuration_id, name, description, data_created) VALUES ('%s', '%s', '%s', '%s')""" % (configuration_id, name, description, data_created)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
def TEST_logs(history_id, name, content, date):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""INSERT INTO test_logs (history_id, name, content, "date") VALUES ('%s','%s','%s','%s')""" % (history_id, name, content, date)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()