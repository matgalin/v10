import time
import json
from datetime import date
from datetime import datetime
from datetime import timedelta
import db_get as db_get
import db_update as db_update
import test_history as test_history
import background as background
import time_conversion as time_conversion

def look_for_errors():
	TEST_history=db_get.TEST_history('all')
	for test in TEST_history:
		if test['is_running']==3:
			db_update.TEST_history(test['id'], 'change_status', 0)

def look_for_finished_tests():
	TEST_history=db_get.TEST_history('all')
	for test in TEST_history:
		if test['is_running']==1:
			#print 1
			now = time_conversion.now_date()
			#now=str(now)
			finish=test['data_planned_end']
			now=time_conversion.date_to_readable(now)
			now=time_conversion.date_to_operate(now)
			try: 
				time_conversion.date_to_operate(finish)
			except:
				return 0
			else:
				finish=time_conversion.date_to_operate(finish)
				if finish<=now:
					background.stop_test(test['id'])


