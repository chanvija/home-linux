#!/usr/bin/python3

import sqlite3
import argparse
import subprocess
import sys

def get_db_data(db_file):
    
    conn = sqlite3.connect(db_file)
    myCursor = conn.cursor()
    myCursor.execute('''SELECT * FROM collection WHERE day = strftime('%d','now') AND month = strftime('%m','now') AND type = "photo"''')
    ret_list = myCursor.fetchall()
    conn.close()
    
    return ret_list

def open_html_header():
    print("Content-type:text/html\r\n\r\n")
    print('<html>')
    print('<head>')
    print('<title>CDJ Daily Album</title>')
    print('</head>')

def open_html_body():
    print('<body>')

def close_html_body():
    print('</body>')

def close_html_header():
    print('</html>')

def print_html(msg):
    print(f'<p>{msg}</p>')
    
def print_href(text,url):
    print(f'<p><a href="{url}">{text}</a></p>')

def get_db_file(archive_directory):
    cmd = 'ls -1 ' + archive_directory + '/*.db'
    db_files = subprocess.getoutput(cmd)
    if len(db_files.split()) == 1:
        #logging.debug(f"Found db file {db_files}")
        return db_files
    else:
        #logging.info("\n"*2 + "More than one db file found. Specify which db file to use using -b option\n")
        #logging.info(db_files + "\n\n")
        parser.print_help()
        print()
        sys.exit()

if __name__ == '__main__':
    
    #log_format = "%(asctime)s: %(levelname)s: %(message)s"
    log_format = "%(levelname)s: %(message)s"
    log_time_format = "%a %d/%b/%Y %I:%M:%S %p"
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--archive_directory",
                        help="photo archive directory")
    parser.add_argument("-b", "--db_file",
                        help="specific sqlite db file to use")
    parser.add_argument("-d", "--debug",
                        help="enable debug messsages", action="store_true")
    args = parser.parse_args()
    
    if args.archive_directory:
        ar_directory = args.archive_directory
    else:
        # ar_directory = "/Volumes/chanvija-time-machine/pictures-archive/"
        ar_directory = "../../pictures-archive/"
        ar_directory_path = "../"
        ar_directory = "pictures-archive/"
    
    if args.debug:
        #logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=log_time_format)
        pass
    else:
        #logging.basicConfig(level=logging.INFO, format=log_format, datefmt=log_time_format)
        pass
        
    if not args.db_file:
        db_file = get_db_file(ar_directory_path + ar_directory)
    else:
        db_file = args.db_file
    
    db_list = get_db_data(db_file)

    open_html_header()
    open_html_body()
    
    try:
        for files in db_list:
            #logging.info(ar_directory + '/' + files[0])
            filename = ar_directory + files[0]
            print_href(files[0].split('/')[-1], f"show_picture.py?filename={filename}")
    except e:
        print_html(e)
    close_html_body()
    close_html_header()

