import db_get as db_get  ## get data from database
import db_update as db_update ##update data in database
from datetime import date
from datetime import datetime
from datetime import timedelta
global FMT
FMT = '%Y-%m-%d %H:%M:%S'
def now_date():
	return datetime.now()
##convert date to operate date	
def date_to_operate(arg):
	global FMT
	return datetime.strptime(arg, FMT)
## convert date to unix date, in s
def date_to_unix(arg):
	global FMT
	return int(date_to_operate(arg).strftime("%s"))
##convert date to string	
def date_to_readable(arg):
	global FMT
	return arg.strftime(FMT)

## add minutes/hours/days to specified time
def add_timedelta(arg, m):
	global FMT
	return arg+timedelta(minutes = int(m))
## calculate difference between two dates
def calc_timedelta(arg1, arg2):
	global FMT
	return date_to_operate(arg1) - date_to_operate(arg2)