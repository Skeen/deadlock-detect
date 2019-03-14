from __future__ import print_function
import threading
from threading import Thread

import sys
import linecache
import random
import time
import string

from threading import Lock


#print_lock = Lock()
#def save_print(*args, **kwargs):
#    with print_lock:
#        print(*args, **kwargs)


def traceit(frame, event, arg):
    if event == "line":
        name = frame.f_globals["__name__"]
        if name == '__main__':
            for i in range(5):
                if shared['schedule'][0] != threading.current_thread().name:
                    break
                time.sleep(0.05)
                # save_print("%s sleeping %d" % (threading.current_thread().name, i))
            # time.sleep(1)
            # save_print(shared['schedule'])
            shared['schedule'] = shared['schedule'][1:]
    return traceit

shared = {}

increment_lock = Lock()
def func1():
    # with increment_lock:
    temp = shared['number']
    temp = temp + 1
    shared['number'] = temp

def func2():
    with increment_lock:
        temp = shared['number']
        temp = temp + 1
        shared['number'] = temp

def main1():
    sys.settrace(traceit)
    func1()

def main2():
    sys.settrace(traceit)
    func2()

import inspect
# TODO: Pull out lines with inspect
lines = 4
num_threads = 2
letters = string.ascii_lowercase
thread_names = letters[:num_threads]

import itertools

for target in [main1, main2]:
    shared['results'] = {}
    print("Testing", target.__name__)
    print("Running all schedules (this will take a while)...")
    schedules = set([x for x in itertools.permutations(thread_names * lines, lines * num_threads)])
    for schedule in sorted(schedules):
        shared['schedule'] = schedule
        shared['number'] = 0
        # Print the current schedule
        # print()
        print(schedule)
        
        threads = []
        for thread in thread_names:
            thread = Thread(target=target, name=thread)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        # Save the result of this run
        shared['results']["".join(schedule)] = shared['number']

        if len(set(v for (k,v) in shared['results'].items())) != 1:
            print("Code NOT OK; Race-condition detected")
            break
    print()
