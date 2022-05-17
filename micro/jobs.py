# -*- coding: utf-8 -*

from micro import config

import threading
import schedule
import logging
import time
import re

  
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
