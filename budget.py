#!/usr/bin/env python3

import datetime
from recurrent import RecurringEvent
import dateutil.rrule

start = datetime.datetime(2014, 12, 5)
end = datetime.datetime(2015, 5, 1)

class Scheduler:
    def __init__(self, start, end):
        """
        :param start: earliest time schedule events may occur, inclusive, and reference time for relative time descriptions
        :param end: latest time schedule events may occur, inclusive
        :return: new `Scheduler` instance
        """
        self.start, self.end = start, end
        self.events = []
        self.recurrent_parser = RecurringEvent(now_date=start)

    def register_event(self, description, data = None):
        """
        Registers an event with the schedule, with a description such as "every feb 2 at noon".

        :param description: English language description of event, which must include a natural language description of when it occurs.
        :param data: arbitrary user data to associate with an event instance
        :return: None
        """
        parsed_rrule = self.recurrent_parser.parse(description)
        assert parsed_rrule is not None, "Could not detect event times from description."
        if isinstance(parsed_rrule, datetime.datetime): # only a single instance of the event, given as a datetime
            self.events.append((parsed_rrule, data))
        else: # RRULE string, find each instance of the event in the current time frame
            assert isinstance(parsed_rrule, str)
            rrule = dateutil.rrule.rrulestr(parsed_rrule)

            # determine the first occurrence of the event, since `rrule.between` below doesn't work if the start time is after the first occurrence
            start = self.start
            if self.recurrent_parser.dtstart is not None:
                start = self.recurrent_parser.dtstart

            for occurrence in rrule.between(start, self.end, inc=True):
                if occurrence >= self.start: # filter out the ones that are before the start time
                    self.events.append((occurrence, data))

    def list_events(self):
        """
        Produces a sorted list of tuples,

        :return: A sorted list of tuples, each containing an event occurrence as a `datetime.datetime` and the event user data.
        """
        return sorted(self.events, key=lambda event: event[0])

s = Scheduler(start, end)

# work stuff
s.register_event("december 19", (1404.17, "Enflick full-time last payment"))
s.register_event("december 19", (140 * 4, "Vacation bonus"))
s.register_event("every 2 weeks from jan 15 2015 to apr 30 2015", (22 * 25 * 0.85, "Enflick part-time payment"))

# rent and housing
s.register_event("on the 1st of every month from dec 1 2014 to apr 30 2015", (-600, "208 Sunview rent"))
s.register_event("on the 1st of every month from dec 1 2014 to apr 30 2015", (-30, "208 Sunview utilities"))
s.register_event("on the 1st of every month from dec 1 2014 to aug 30 2015", (-575, "88A McDougall rent"))

s.register_event("18th every month", (-400, "Food/grocery"))
s.register_event("1st every month", (-50, "Mutual funds"))
s.register_event("10th every month", (-30, "Phone bill"))
s.register_event("18th every month", (-100, "Personal"))

balance = 2778.05

times, balances = [], []
for event in s.list_events():
    time, (amount, description) = event

    times.append(time)
    balances.append(balance)

    balance += amount

    times.append(time)
    balances.append(balance)
    print("{} {:>30} {:10.2f} {:12.2f}".format(time, description, amount, balance))

import matplotlib.pyplot as plt

# red dashes, blue squares and green triangles
axis = plt.gca()
axis.plot(times, balances, "-")
axis.set_title("Balance")
axis.grid(True)
plt.show()
