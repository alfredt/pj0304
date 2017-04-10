# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:38:05 2017

@author: user
"""

from datetime import datetime, timedelta

def date_parser(string):
    string = str(string)
    if "minutes" in string or "minute" in string:
        string = string.split()
        now = datetime.now() - timedelta(minutes=int(string[0]))
        return now.strftime("%Y-%m-%d")
    elif "hours" in string or "hour" in string:
        string = string.split()
        now = datetime.now() - timedelta(hours=int(string[0]))
        return now.strftime("%Y-%m-%d")
    elif "days" in string or "day" in string:
        string = string.split()
        now = datetime.now() - timedelta(days=int(string[0]))
        return now.strftime("%Y-%m-%d")
    else:
        datetime_object = datetime.strptime(string, "%d %b %Y").date()
        return datetime_object.strftime("%Y-%m-%d")
        
#print date_parser("23 minutes ago")
#print date_parser("1 hour ago")
#print date_parser("1 day ago")
#print date_parser("5 days ago")
#print date_parser("20 Feb 2017")