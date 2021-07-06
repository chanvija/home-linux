#!/usr/bin/python3

import sqlite3
import argparse
import subprocess
import sys
import urllib.parse
import re

def get_db_data(db_file):
    
    conn = sqlite3.connect(db_file)
    myCursor = conn.cursor()
    myCursor.execute('''SELECT * FROM collection WHERE day = strftime('%d','now', 'localtime') AND month = strftime('%m','now', 'localtime') AND type LIKE "%photo%" ORDER by year,filename''')
    ret_list = myCursor.fetchall()
    conn.close()
    
    return ret_list

def get_my_ip():
    interface = subprocess.getoutput("ip -o route get 142.250.77.164 | perl -nle 'if ( /dev\s+(\S+)/ ) {print $1}'")
    ip = subprocess.getoutput(f'ifconfig {interface} | egrep -o "inet \S+" | cut -d" " -f 2')
    return(ip)

def open_html_header():
    print("Content-type:text/html\r\n\r\n")
    print('<html>')
    print('<head>')
    print('<title>CDJ Daily Album</title>')
    print('<link rel="stylesheet" href="../css/test.css">')
    print('</head>')

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
        #relative to cgi-bin directory
        db_directory = "../html/pictures/"
        picture_directory = "pictures/"
    
    if args.debug:
        #logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=log_time_format)
        pass
    else:
        #logging.basicConfig(level=logging.INFO, format=log_format, datefmt=log_time_format)
        pass
        
    if not args.db_file:
        db_file = get_db_file(db_directory)
    else:
        db_file = args.db_file
    
    db_list = get_db_data(db_file)
    ip = get_my_ip()
    
    print("Content-type:text/html\r\n\r\n")
    print('''
    <html>
        <head>
            <link rel="stylesheet" href="../css/test.css" type="text/css">
            <title>
                CDJ Daily Reminisce
            </title>
            <script language="JavaScript" type="text/javascript" src="../js/jquery-3.3.1.min.js"></script>
            <script language="JavaScript" type="text/javascript" src="../js/cdj-funcs.js"></script>
            <style>
                
            </style>
        </head>
        <body>
            <div id="container" class="container_div">
                <div id="top" class="top_div">
                    <div id="left" class="left">
                        <ul class="background"> ''')
            
    year_done = []
    
    for files in db_list:
        #logging.info(ar_directory + '/' + files[0])
        if not re.match(".*photo.*", files[5]):
            #skip video files due to size.  
            continue
        
        filename = f"http://{ip}/{picture_directory}{files[0]}"
        if files[1] not in year_done: 
            print(f"<h1>{files[1]}</h1>")
            year_done.append(files[1])
        href_string = ".".join(files[0].split('/')[-1].split(".")[:-1])
        # print_href(href_string, f"{filename}")
        t = files[0].split("/")[2]
        tag_line = urllib.parse.quote("Tags - " + files[-1], safe='~()*!.\'')
        print(f'<li> <a href="#" onclick=test_show_picture("{filename}","{tag_line}")>{t}</a></li>')

    print('''
                        </ul>
                    </div>
                    <div class="photo_area" id=right1>
                        Select a photo link on the left
                    </div>
                    <div class="tag_area" id=right2>
                        Add a new tag <br>to this photo
                    </div>
                </div>
                <div id="bottom" class="bottom_div"> 
                    Add a tag to this photo <br> 
                    <input type="text" id="add_tag" name="add_tag"><br>
                    <button type="button">Add tag</button> 
                </div>
            </div>
        </body>
    </html>''')
