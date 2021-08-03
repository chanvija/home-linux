#!/usr/bin/python3

import sqlite3
from subprocess import Popen
import datetime

def main():
    db_file = "/usr/local/var/www/home-linux-www/html/cdj-album.db"
    conn = sqlite3.connect(db_file)
    myCursor = conn.cursor()
    for yy in range(2001,2022):
        print(yy)
        myCursor.execute('SELECT filename,tags FROM collection where year = "' + str(yy) + '"')
        temp = myCursor.fetchall()
        for t in temp:
            y = t[0].split("/")[0]
            z = t[1] + "," + y
            print(f"{t[0]} ... {t[1]} ... {z}")
            myCursor.execute('UPDATE collection SET tags="' + z + '" WHERE filename = "' + t[0] + '"')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
