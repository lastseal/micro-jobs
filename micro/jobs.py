# -*- coding: utf-8 -*

from micro import config

import threading
import schedule
import logging
import time
import sys
import re

immediately = '--immediately' in sys.argv[1:]

##
#

def monday(at_time):

    def decorator(handle):
        schedule.every().monday.at(at_time).do(handle)

        logging.debug("every monday at %s", at_time)

        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as ex:
                logging.error(ex)

    return decorator

##
#

def daily(at_time, timezone, immediately=immediately):

    def decorator(handle):
        
        schedule.every().day.at(at_time, timezone).do(handle)

        logging.debug("every day at %s", at_time)

        if immediately:
            handle()

        while True:
            schedule.run_pending()
            time.sleep(1)

    return decorator

##
#

def every(value, immediately=immediately):

    matches = re.findall("(.*)(s|m|h|d)", value)

    if not matches:
        raise Exception(f"Format not support {every}")

    def decorator(handle):
        
        job = schedule.every( int(matches[0][0]) )

        unit = matches[0][1]
        
        if unit == "s":
            job.seconds.do(handle)
        elif unit == "m":
            job.minutes.do(handle)
        elif unit == "h":
            job.hours.do(handle)
        else:
            job.days.do(handle)
            
        logging.debug("every %s", value)

        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as ex:
                logging.error(ex)

    return decorator

##
# Schedule

def repeat(args, thread=False):
    def decorator(handle):

        every = args["every"]

        if every == "day":
            scheduler = schedule.every().day
        elif every == "hour":
            scheduler = schedule.every().hour
        elif every == "minute":
            scheduler = schedule.every().minute
        else:
            matches = re.findall("(.*)(s|m|h|d)", every)
            
            if not matches:
                raise Exception(f"Format not support {every}")

            e = schedule.every( int(matches[0][0]) )

            t = matches[0][1]

            if t == "s":
                scheduler = e.seconds
            elif t == "m":
                scheduler = e.minutes
            elif t == "h":
                scheduler = e.hours
            elif t == "d":
                scheduler = e.days
            else:
                raise Exception(f"Format not support {every}")

        def job():
            try:
                handle()
            except Exception as ex:
                logging.error(ex)
        
        if "at" in args:
            scheduler.at(args['at']).do(job)
        else:
            scheduler.do(job)

        logging.info("starting %s", args)

        def target():
            while True:
                schedule.run_pending()
                time.sleep(1)

        if not thread:
            target()
        else:
            threading.Thread(target=target, daemon=True).start()
        
    return decorator
