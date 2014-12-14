#!/usr/bin/env python3

import datetime
from recurrent import RecurringEvent
from dateutil import rrule

start_time = datetime.datetime(2014, 12, 14)

r = RecurringEvent(now_date=start_time)

parsed_rrule = r.parse('1st every month from december to april 30')
assert parsed_rrule is not None


print(r.parse('not a date at all'))