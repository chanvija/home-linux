from flask import Flask, request, jsonify, make_response, render_template
import sqlite3
import os
import json

app = Flask(__name__)

db_file = "/usr/local/var/www/home-linux-www/html/cdj-album.db"
if not os.path.isfile(db_file):
    db_file = "/var/www/html/pictures-archive/cdj-album.db"

@app.route('/get_unique_tags',methods = ['GET', 'POST', 'OPTIONS'])
def get_unique_tags():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return(response)
    elif ( request.method == 'POST' or request.method == "GET" ):
        data = request.get_json()    
        conn = sqlite3.connect(db_file)
        myCursor = conn.cursor()
        myCursor.execute('SELECT DISTINCT tags FROM collection')
        temp = myCursor.fetchall()
        tag_list = {}
        tag_list['tags'] = []
        for t in temp:
            for t1 in t[0].split(","):
                if not t1 in tag_list['tags']:
                    tag_list['tags'].append(t1)

        tag_list['tags'] = sorted(tag_list['tags'])

        print(f"Unique tag list : {tag_list}")
        return(tag_list)

@app.route('/get_archive_directory',methods = ['POST', 'OPTIONS'])
def get_archive_directory():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return(response)
    elif request.method == 'POST':
        dir_prefix = "../../pictures-archive/"
        if not os.path.isdir(dir_prefix):
            dir_prefix = "pictures-archive/"
        
        print(f"dir_path = {dir_prefix}")
        dir_prefix = jsonify(dir_prefix=dir_prefix)
        dir_prefix.headers.add("Access-Control-Allow-Origin", "*") 
        return(dir_prefix)

@app.route('/update_file',methods = ['POST', 'OPTIONS'])
def update_file():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return(response)
    elif request.method == 'POST':
        data = request.get_json()    
        print(data.keys())    
        new_tag = data['new_tag']
        filter = data['filter']
        filter_type = data['filter_type']
        conn = sqlite3.connect(db_file)
        myCursor = conn.cursor()
        if filter_type == "file_single":
            myCursor.execute('SELECT filename,tags FROM collection where filename = "' + filter + '"')
            temp = myCursor.fetchall()
            print(f"... old tag {temp[0][1]}")
            if new_tag not in temp[0][1].split(","):
                for t in temp[0][1].split(","):
                    new_tag =  new_tag + "," + str(t) if t else new_tag
                print(f"... new tag {new_tag}")
                myCursor.execute('UPDATE collection SET tags="' + new_tag + '" WHERE filename = "' + filter + '"')
                conn.commit()
                myCursor.execute('SELECT tags FROM collection where filename = "' + filter + '"')
                new_current_tags = myCursor.fetchall()
                retval = jsonify(result=True, old_tag=temp[0][1],  updated_tag=new_current_tags[0][0], error=None)
            else:
                print(f"New tag : '{new_tag}'' already exists for this file {filter} Existing tags : {temp[0][1]}")
                retval = jsonify(result=False, error="Tag already exists")
                        
            conn.close()
        else:
            conn.close()
            return(jsonify(result=False, error=f"Unknown filter_type {request.form['filter_type']}"))
                   
        retval.headers.add("Access-Control-Allow-Origin", "*") 
        return(retval)
        
            
@app.route('/get_row',methods = ['POST', 'OPTIONS'])
def get_row():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return(response)
    elif request.method == 'POST':
        data = request.get_json()        
        tag = data['tag'].lower()
        count = data['count']
        offset = data['offset']
        query_type = data['query_type']
        conn = sqlite3.connect(db_file)
        myCursor = conn.cursor()
        if tag == "today":
            cmd = f'SELECT filename,tags FROM collection WHERE day = strftime("%d","now", "localtime") AND month = strftime("%m","now", "localtime") AND type LIKE "%photo%" and tags NOT LIKE "%delete%" ORDER by year,filename LIMIT {count} OFFSET {offset}'
            cmd2 = f'SELECT count(*) FROM collection WHERE day = strftime("%d","now", "localtime") AND month = strftime("%m","now", "localtime") AND type LIKE "%photo%" and tags NOT LIKE "%delete%" ORDER by year,filename'

        elif query_type == "date":
            yy = data['year']
            mm = data['month'].lower()
            cmd = f'SELECT filename,tags FROM collection WHERE year = {yy} AND tags LIKE "%{mm}%" AND type LIKE "%photo%" and tags NOT LIKE "%delete%" ORDER by year,filename LIMIT {count} OFFSET {offset}'    
            cmd2 = f'SELECT count(*) FROM collection WHERE year = {yy} AND tags LIKE "%{mm}%" AND type LIKE "%photo%" and tags NOT LIKE "%delete%" ORDER by year,filename'    

        else:
            cmd = f'SELECT filename,tags FROM collection where tags LIKE "%{tag}%" AND type LIKE "%photo%" and tags NOT LIKE "%delete%" LIMIT {count}  OFFSET {offset}'
            cmd2 = f'SELECT count(*) FROM collection where tags LIKE "%{tag}%" AND type LIKE "%photo%" and tags NOT LIKE "%delete%"'
        print(cmd)
        myCursor.execute(cmd)
        temp = myCursor.fetchall()
        print(f"... rows : {temp}")
        
        print(cmd2)
        myCursor.execute(cmd2)
        temp2 = myCursor.fetchall()
        print(f"... row_count : {temp2[0][0]}")
        
        file_list = []
        for t in temp:
            file_list.append((t[0], t[1]))
        conn.close()
        print(f"..{file_list}..")
        retval = jsonify(file_list=file_list, row_count=temp2[0][0])
        retval.headers.add("Access-Control-Allow-Origin", "*") 
        return(retval)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
    
