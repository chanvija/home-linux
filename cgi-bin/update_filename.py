#!/usr/bin/python3

import sqlite3
from subprocess import Popen
import datetime

def main():
    db_file = "/usr/local/var/www/home-linux-www/html/cdj-album.db"
    conn = sqlite3.connect(db_file)
    myCursor = conn.cursor()

    myCursor.execute('SELECT * FROM collection where filename LIKE "%-.jpg%"')
    temp = myCursor.fetchall()
    for t in temp:
        suffix = t[0].split(".")[-1]
        new_filename = "-".join(t[0].split("-")[0:-1]) + "." + suffix
        cmd = '''INSERT INTO collection(filename,year,month,day,tags,type) 
                          VALUES(?,?,?,?,?,?)'''
        new_row = (new_filename, t[1], t[2], t[3], t[4], t[5])
        try:
            myCursor.execute(cmd, new_row)
        except sqlite3.IntegrityError:
            cmd = f"SELECT * FROM collection WHERE filename LIKE '%{new_filename}%'"
            myCursor.execute(cmd)
            temp1 = myCursor.fetchall()
            if t == temp1[0]:
                print(f"FAILED MATCHED : {t[0]} ... {new_filename} ... {t[1]} ... {t[2]} ... {t[3]} ... {t[4]} ... {t[5]}")
            else:
                new_tags = t[4] + "," + "delete"
                cmd = f'UPDATE collection SET tags = "{new_tags}" WHERE filename = "{t[0]}"'
                print(f"UPDATING       : {t[0]} ... {new_filename} ... {t[1]} ... {t[2]} ... {t[3]} ... {t[4]} ... {new_tags}... {t[5]}")
                myCursor.execute(cmd)

        else:
            print(f"PASSED : {t[0]} ... {new_filename} ... {t[1]} ... {t[2]} ... {t[3]} ... {t[4]} ... {t[5]}")

        conn.commit()

    conn.close()

if __name__ == '__main__':
    main()
