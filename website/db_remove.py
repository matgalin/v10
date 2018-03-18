from flask import jsonify, json
import psycopg2
import time
import os
from datetime import datetime
import password as password
login=password.db
###########################################
#### PROV
#########################################
###  Delete Provisioning configuration
def PROV_configuration(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM prov_configuration WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	PROV_ipv4(id)
	PROV_ipv6(id)
	PROV_cm(id)
	

###  Delete Provisioning configuration ipv4
def PROV_ipv4(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM prov_ipv4 WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	

###  Delete Provisioning configuration ipv6
def PROV_ipv6(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM prov_ipv6 WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()		
	
###  Delete Provisioning configuration cable modem config
def PROV_cm_single(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM prov_cm WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	
###  Delete Provisioning configuration cable modem config
def PROV_cm(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM prov_cm WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()

###########################################
#### cm
#########################################
###  Delete Cable Modem Configuration
def CM_configuration(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM cm_configuration WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	CM_part(id)
###  Delete Part of Cable Modem configuration
def CM_part(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM cm_part WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()		

##############################################
###########CCAP NEW
##############################################
def CCAP_configuration_new(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_configuration_new WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	CM_part(id)
###  Delete Part of Cable Modem configuration
def CCAP_part(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_part WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	

##############################################
###########CCAP
##############################################
###  Delete CCAP Configuration
def CCAP_configuration(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_configuration WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	
	CCAP_ds_bond(id)
	CCAP_ds_channel(id)
	CCAP_ds_channel_ofdm(id)
	CCAP_us_channel(id)
	CCAP_us_bond(id)
	
###  Delete CCAP ds bond
def CCAP_ds_bond(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_ds_bond WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
###  Delete CCAP ds channel	
def CCAP_ds_channel(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_ds_channel WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	

###  Delete CCAP ds ofdm channel	
def CCAP_ds_channel_ofdm(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_ds_channel_ofdm WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	

###  Delete CCAP us channel	
def CCAP_us_channel(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_us_channel WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	

###  Delete CCAP us bond
def CCAP_us_bond(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_us_bond WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	
	
##############################################
###########CCAP-< remove single elements
##############################################
	
###  Delete CCAP ds bond
def CCAP_ds_bond_single(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_ds_bond WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
###  Delete CCAP ds channel	
def CCAP_ds_channel_single(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_ds_channel WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	

###  Delete CCAP ds ofdm channel	
def CCAP_ds_channel_ofdm_single(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_ds_channel_ofdm WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	

###  Delete CCAP us channel	
def CCAP_us_channel_single(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_us_channel WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()	

###  Delete CCAP us bond
def CCAP_us_bond_single(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM ccap_us_bond WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()		
	

##############################################
###########TEST
##############################################
###  Delete TEST Configuration
def TEST_configuration(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM test_configuration WHERE id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
	TEST_history(id)
	
def TEST_history(id):
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM test_history WHERE configuration_id='%s'""" % (id)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()
def delete_log():
	conn = psycopg2.connect(login)
	cur = conn.cursor()
	sql="""DELETE FROM test_logs WHERE 1=1"""
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()