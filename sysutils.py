import os
import datetime


def purge_directory(path, days):
    """Delete files in the given path that are older than
    the supplied number of days"""
    for f in os.listdir(path):
        fullpath = os.path.join(path, f)
        timestamp = os.stat(fullpath).st_ctime
        createtime = datetime.datetime.fromtimestamp(timestamp)
        now = datetime.datetime.now()
        delta = now - createtime
        if os.path.isfile(fullpath) and delta.days > days:
            os.remove(fullpath)
