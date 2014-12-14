#!/usr/bin/env python3

import datetime
from recurrent import RecurringEvent

r = RecurringEvent(now_date=datetime.datetime(2010, 1, 1))
print(r.parse('every day starting next tuesday until feb'))

print(r.parse('feb 2nd'))

print(r.parse('not a date at all'))