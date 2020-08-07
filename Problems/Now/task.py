from datetime import datetime
import datetime

# create now_time here
now_time = datetime.datetime.now()
print(now_time)
new_date = datetime.datetime.strptime('24-01-2020', '%d-%m-%Y').date()
# return a datetime corresponding to date_string, parsed according to format.
# Format example: '%Y-%m-%d' - '2020-04-24'
print(new_date)
