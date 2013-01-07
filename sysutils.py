import os
import datetime
import string
from ctypes import windll
import subprocess


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


def get_drives():
    """Get a list of 'in-use' drive letters"""
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives


def get_free_drive_letter():
    """Get a drive letter that is free for use"""
    letters = set(string.uppercase)
    used = set(get_drives())
    return list(letters - used)[-1]


def map_drive(server, share, user=None, password=None):
    """Map a drive to the given windows share, optionally using username
    and password"""
    letter = get_free_drive_letter()
    command = r'net use %s: \\%s\%s' % (letter, server, share)
    if user and password:
        command += r' /u:%s %s' % (user, password)
    subprocess.check_call(command.split(' '), stdout=None, stderr=None)
    return letter


def disconnect_drive(letter):
    command = r'net use /DEL %s:' % letter
    subprocess.check_call(command.split(' '), stdout=None, stderr=None)
