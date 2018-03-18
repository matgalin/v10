import db_insert as db_insert ##update data in database
from datetime import date
from datetime import datetime
import time_conversion as time_conversion

## starting test: get current datetime and put it into database. 
def insert_log(TEST_history, name, content):
	id=TEST_history[0]['id']
	now=time_conversion.now_date()
	date=time_conversion.date_to_readable(now)
	db_insert.TEST_logs(id, name, content, date)

