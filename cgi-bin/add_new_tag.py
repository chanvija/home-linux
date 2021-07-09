#!/usr/bin/python3

import sqlite3
from subprocess import Popen
import datetime

def main():
    with open("/tmp/abcd123", "a") as t:
        t.write(str(datetime.datetime.now())+"\n")

if __name__ == '__main__':
    main()