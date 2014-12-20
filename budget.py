#!/usr/bin/env python3

from datetime import datetime, date, time

from scheduler import Scheduler

start = datetime.combine(date.today(), datetime.min.time()) # the very start of today
end = datetime(2015, 5, 1)
balance = 4000

# enable cross-platform console coloration using the standard ANSI character sequences
from colorama import init, Fore, Back, Style
init()

s = Scheduler(start, end)

# work stuff
s.register("every 2 weeks from jan 15 2015 to apr 30 2015", (700 * 0.85, "Part-time job"))

# rent and housing
s.register("on the 1st of every month from dec 1 2014 to apr 30 2015", (-600, "Rent"))
s.register("on the 1st of every month from dec 1 2014 to apr 30 2015", (-60, "Utilities"))

s.register("19th every month", (-400, "Food/grocery"))
s.register("1st every month", (-150, "Investments"))
s.register("10th every month", (-30, "Phone bill"))
s.register("19th every month", (-400, "Personal"))

running_balance = 0
for event in [(start, (balance, "START"))] + s.list_events():
    time, (amount, description) = event
    running_balance += amount
    print("{}{time}{reset} {}{description:30}{reset} {}{amount:9.2f}{reset} {}{balance:9.2f}{reset}".format(
        Fore.WHITE + Back.BLACK + Style.DIM,
        Fore.BLACK + Back.WHITE + Style.BRIGHT,
        Fore.BLACK + (Back.RED if amount < 0 else Back.GREEN) + Style.NORMAL,
        Fore.BLACK + (Back.RED if balance < 0 else Back.GREEN) + Style.NORMAL,
        reset=Fore.WHITE + Back.BLACK + Style.NORMAL,
        time=time, description=description, amount=amount, balance=running_balance
    ))
