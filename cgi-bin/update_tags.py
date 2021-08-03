#!/usr/bin/python3

import sqlite3
from subprocess import Popen
import datetime

def main():
    db_file = "/usr/local/var/www/home-linux-www/html/cdj-album.db"
    conn = sqlite3.connect(db_file)
    myCursor = conn.cursor()

    myCursor.execute('SELECT * FROM collection where tags LIKE "%delete%"')
    temp = myCursor.fetchall()
    for t in temp:
        new_tags = t[4].replace("delete,","")
        cmd = f'UPDATE collection SET tags = "{new_tags}" WHERE filename = "{t[0]}"'
        print(f"UPDATING       : {t[0]} ... {t[1]} ... {t[2]} ... {t[3]} ... {t[4]} ... {new_tags}... {t[5]}")
        myCursor.execute(cmd)

        conn.commit()

    conn.close()

if __name__ == '__main__':
    main()
