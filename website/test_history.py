import db_get as db_get  ## get data from database
import db_update as db_update ##update data in database
from datetime import date
from datetime import datetime
from datetime import timedelta
import time_conversion as time_conversion

## starting test: get current datetime and put it into database. 
def start_prepare(TEST_history):
	id=TEST_history[0]['id']
	db_update.TEST_history(id, 'change_status', 3)
def error(TEST_history):
	id=TEST_configuration[0]['id']
	db_update.TEST_history(id, 'change_status', 4)
def start(TEST_history, zabbix_group_id, grafana_dashboard_uid, interval):
	id=TEST_history[0]['id']
	now = time_conversion.now_date()
	now_plus_interval=time_conversion.add_timedelta(now, interval)
	now=time_conversion.date_to_readable(now)
	now_plus_interval=time_conversion.date_to_readable(now_plus_interval)
	db_update.TEST_history(id, 'start', str(now))
	db_update.TEST_history(id, 'planned_end', str(now_plus_interval))
	db_update.TEST_history(id, 'zabbix', zabbix_group_id)
	db_update.TEST_history(id, 'grafana', grafana_dashboard_uid)
##stoping test. get current datetime and put it into database. also calculate interval	
def stop(TEST_history):
	id=TEST_history[0]['id']
	now = time_conversion.now_date()
	now=time_conversion.date_to_readable(now)
	tdelta=time_conversion.calc_timedelta(now, TEST_history[-1]['data_start'])
	#tdelta = datetime.strptime(str(now), FMT) - datetime.strptime(str(TEST_history[-1]['data_start']), FMT)
	db_update.TEST_history(id, 'stop', str(now))
	db_update.TEST_history(id, 'interval', str(tdelta))
		

