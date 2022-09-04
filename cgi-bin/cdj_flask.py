from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
from time import sleep
import sqlite3
import os
import json
import pymongo
from bson import json_util
import re
import datetime

app = Flask(__name__)
CORS(app)

db_file = "/data1/pictures-archive/cdj-album.db"
if not os.path.isfile(db_file):
    #db_file = "/var/www/html/cdj-album.db"
    pass

def get_location(create_time,latitude,longitude):
    if latitude is not None and longitude is not None:
        ret_value = get_gps_location_info(latitude,longitude)
    else:
        ret_value = get_date_location_info(create_time)
    return(ret_value)

def get_gps_location_info(latitude,longitude):
    url = f'https://nominatim.openstreetmap.org/reverse/?format=geocodejson&lat={latitude}&lon={longitude}'
    print(url)
    data = requests.get(url).json()
    if "error" in data:
        return(None)
    country = gps_data_clean(data['features'][0]['properties']['geocoding'].get('country',''))
    state = gps_data_clean(data['features'][0]['properties']['geocoding'].get('state',''))
    county = gps_data_clean(data['features'][0]['properties']['geocoding'].get('county',''))
    city = gps_data_clean(data['features'][0]['properties']['geocoding'].get('city',''))
    district = gps_data_clean(data['features'][0]['properties']['geocoding'].get('district',''))
    locality = gps_data_clean(data['features'][0]['properties']['geocoding'].get('locality',''))
    location = '-'.join(filter(lambda x: x != '', [country,state,county,city,district,locality]))
    return(location)

def get_date_location_info(date_time):
    print(f'opening {db_file}')
    conn = sqlite3.connect(db_file)
    mycursor = conn.cursor()
    ret_value = None
    pattern = ''
    for i in range(11,len(date_time)+1):
        if pattern != '':
            pattern +=  ' OR '
        pattern += f'"date-time" LIKE "{date_time[0:i]}%"'
    cmd = f'SELECT COUNT(*),location FROM gps_data WHERE ({pattern}) ORDER BY "date-time" LIMIT 1'
    print(cmd)
    mycursor.execute(cmd)
    ret_value = None
    temp = mycursor.fetchall()
    if temp[0][0] > 0:
        ret_value = temp[0][1]
    mycursor.close()
    conn.close()
    print(ret_value)
    return(ret_value)

@app.route('/stream')
def stream():
    def generate():
        with open('/var/log/system.log') as f:
            while True:
                yield f.read()
                sleep(1)

    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return(response)
    elif ( request.method == 'POST' or request.method == "GET" ):
        retval = make_response()
        retval.headers.add("Access-Control-Allow-Origin", "*") 
        retval = jsonify(log_lines=generate())
        return app.response_class(retval, mimetype='text/plain')

@app.route('/get_latest_tags',methods = ['GET', 'POST', 'OPTIONS'])
def get_latest_tags():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return(response)
    elif ( request.method == 'POST' or request.method == "GET" ):
        print(f'opening {db_file}')
        conn = sqlite3.connect(db_file)
        myCursor = conn.cursor()
        today = datetime.datetime.now().strftime('%-Y-%-m-%-d')
        myCursor.execute('SELECT DISTINCT tag FROM tag_table WHERE last_used = "' + today + '"')
        temp = myCursor.fetchall()
        tag_list = []
        for t in sorted(temp):
            if t[0] != "":
                tag_list.append(t[0])

        retval = make_response()
        retval.headers.add("Access-Control-Allow-Origin", "*") 
        retval = jsonify(tag_list=tag_list)
        return(retval)

@app.route('/get_unique_tags',methods = ['GET', 'POST', 'OPTIONS'])
def get_unique_tags():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return(response)
    elif ( request.method == 'POST' or request.method == "GET" ):
        print(f'opening {db_file}')
        conn = sqlite3.connect(db_file)
        myCursor = conn.cursor()

        #myCursor.execute('SELECT DISTINCT user_tags FROM collection WHERE user_tags NOT LIKE "%delete%" and user_tags NOT LIKE ""')
        myCursor.execute('SELECT DISTINCT user_tags FROM collection WHERE user_tags NOT LIKE ""')
        temp = myCursor.fetchall()
        tag_list = []
        for t in temp:
            for t1 in t[0].split(":"):
                if not t1 in tag_list:
                    tag_list.append(t1)

        #myCursor.execute('SELECT DISTINCT tags FROM collection WHERE user_tags NOT LIKE "%delete%" and tags NOT LIKE ""')
        myCursor.execute('SELECT DISTINCT tags FROM collection WHERE tags NOT LIKE ""')
        temp = myCursor.fetchall()
        for t in temp:
            for t1 in t[0].split(":"):
                x = re.match('20\d\d',t1)
                if x or t1.isalpha():
                    if not t1 in tag_list:
                        tag_list.append(t1)

        tag_list = sorted(tag_list)

        retval = make_response()
        retval.headers.add("Access-Control-Allow-Origin", "*") 
        retval = jsonify(tag_list=tag_list)
        return(retval)

@app.route('/get_archive_directory',methods = ['POST', 'OPTIONS'])
def get_archive_directory():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return(response)
    elif request.method == 'POST':
        dir_prefix = "/data1/pictures-archive/"
        if not os.path.isdir(dir_prefix):
            dir_prefix = "pictures-archive/"
        
        #dir_prefix = make_response()
        dir_prefix = jsonify(dir_prefix=dir_prefix)
        dir_prefix.headers.add("Access-Control-Allow-Origin", "*") 
        return(dir_prefix)

@app.route('/update_file',methods = ['POST', 'OPTIONS'])
def update_file():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return(response)
    elif request.method == 'POST':
        data = request.get_json()    
        action = data['action'].lower()
        new_tag_list = data['action_value'].lower()
        replace_tag = data['replace_tag'].lower()
        filter = data['filter']
        filter_type = data['filter_type']
        print(f'opening {db_file}')
        conn = sqlite3.connect(db_file)
        myCursor = conn.cursor()
        retval = make_response()
        retval.headers.add("Access-Control-Allow-Origin", "*") 
        if filter_type == "file_single":
            myCursor.execute('SELECT filename,user_tags FROM collection where filename = "' + filter + '"')
            temp = myCursor.fetchall()
            tag_exists = False
            exists_tag_list = []
            if replace_tag == 'false':
                updated_tag = str(temp[0][1])
            else:
                updated_tag = ""
            if action == "clear":
                new_tag = ""
                updated_tag = ""
            for new_tag in new_tag_list.split(","):
                if new_tag not in updated_tag.split(":"):
                    updated_tag = updated_tag + ":" + new_tag
                else:
                    tag_exists = True
                    exists_tag_list.append(new_tag)
            updated_tag = updated_tag.lstrip(':')
            updated_tag = updated_tag.rstrip(':')
            today = datetime.datetime.now().strftime('%-Y-%-m-%-d')
            for ntag in updated_tag.split(':'):
                a = myCursor.execute(f'REPLACE INTO tag_table (tag,last_used) VALUES ("{ntag}","{today}")')
                b = conn.commit()
                a = myCursor.execute(f'UPDATE tag_table SET last_used="{today}" WHERE tag = "{ntag}"')
                b = conn.commit()
            myCursor.execute('UPDATE collection SET user_tags="' + updated_tag + '" WHERE filename = "' + filter + '"')
            conn.commit()
            myCursor.execute('SELECT user_tags FROM collection where filename = "' + filter + '"')
            new_current_tags = myCursor.fetchall()
            retval = jsonify(result=True, old_tag=temp[0][1],  updated_tag=new_current_tags[0][0], error=None)
            conn.close()
        else:
            conn.close()
            ret_val = jsonify(result=False, error=f"Unknown filter_type {request.form['filter_type']}")
                   
        return(retval)
        
            
@app.route('/get_row',methods = ['POST', 'OPTIONS'])
def get_row():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return(response)
    elif request.method == 'POST':
        data = request.get_json()        
        print(json_util.dumps(data, indent=4))
        if not isinstance(data['tag'],list):
            if ',' in data['tag']:
                tag_list = data['tag'].lower().split(',')
                tag = ''
            else:
                tag = data['tag']
        else:
            tag_list = data['tag']
            tag = ''
        show_deleted = data['show_deleted'].lower()
        count = data['count']
        offset = data['offset']
        query_type = data['query_type']
        print(f'opening {db_file}')
        conn = sqlite3.connect(db_file)
        myCursor = conn.cursor()
        if tag == "today":
            if show_deleted == 'false':
                cmd = f'SELECT filename,tags,user_tags,create_time,latitude,longitude,location,size,size_units FROM collection WHERE day = strftime("%d","now", "localtime") AND month = strftime("%m","now", "localtime") AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%" ORDER by year,filename LIMIT {count} OFFSET {offset}'
                cmd2 = f'SELECT count(*) FROM collection WHERE day = strftime("%d","now", "localtime") AND month = strftime("%m","now", "localtime") AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%" ORDER by year,filename'
            else:
                cmd = f'SELECT filename,tags,user_tags,create_time,latitude,longitude,location,size,size_units FROM collection WHERE day = strftime("%d","now", "localtime") AND month = strftime("%m","now", "localtime") AND type LIKE "%photo%" ORDER by year,filename LIMIT {count} OFFSET {offset}'
                cmd2 = f'SELECT count(*) FROM collection WHERE day = strftime("%d","now", "localtime") AND month = strftime("%m","now", "localtime") AND type LIKE "%photo%" ORDER by year,filename'

        elif query_type == "date":
            yy = data['year']
            mm = data['month'].lstrip('0')
            dd = data['day']
            ignore_year = data['ignore_year']
            if ignore_year == 'false':
                if show_deleted == 'false':
                    cmd = f'SELECT filename,tags,user_tags,create_time,latitude,longitude,location,size,size_units FROM collection WHERE month = {mm} AND day = {dd} AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%" ORDER by year,filename LIMIT {count} OFFSET {offset}'    
                    cmd2 = f'SELECT count(*) FROM collection WHERE month = {mm} AND day = {dd} AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%" ORDER by year,filename'    
                else:
                    cmd = f'SELECT filename,tags,user_tags,create_time,latitude,longitude,location,size,size_units FROM collection WHERE month = {mm} AND day = {dd} AND type LIKE "%photo%" ORDER by year,filename LIMIT {count} OFFSET {offset}'    
                    cmd2 = f'SELECT count(*) FROM collection WHERE month = {mm} AND day = {dd} AND type LIKE "%photo%" ORDER by year,filename'    
            else:
                if show_deleted == 'false':
                    cmd = f'SELECT filename,tags,user_tags,create_time,latitude,longitude,location,size,size_units FROM collection WHERE month = {mm} AND day = {dd} AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%" ORDER by year,filename LIMIT {count} OFFSET {offset}'    
                    cmd2 = f'SELECT count(*) FROM collection WHERE month = {mm} AND day = {dd} AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%" ORDER by year,filename'    
                else:
                    cmd = f'SELECT filename,tags,user_tags,create_time,latitude,longitude,location,size,size_units FROM collection WHERE month = {mm} AND day = {dd} AND type LIKE "%photo%" ORDER by year,filename LIMIT {count} OFFSET {offset}'    
                    cmd2 = f'SELECT count(*) FROM collection WHERE month = {mm} AND day = {dd} AND type LIKE "%photo%" ORDER by year,filename'    

        else:
            if tag == "delete":
                cmd = f'SELECT filename,tags,user_tags,create_time,latitude,longitude,location,size,size_units FROM collection where (tags LIKE "%{tag}%" OR user_tags LIKE "%{tag}%") AND type LIKE "%photo%" LIMIT {count}  OFFSET {offset}'
                cmd2 = f'SELECT count(*) FROM collection where (tags LIKE "%{tag}%" OR user_tags LIKE "%{tag}%") AND type LIKE "%photo%"'
            else:
                tag_cmd = ''
                for tag in tag_list:
                    if tag_cmd == '':
                        tag_cmd += f'(tags like "%{tag}%" OR user_tags LIKE "%{tag}%") '
                    else:
                        tag_cmd += f'AND (tags like "%{tag}%" OR user_tags LIKE "%{tag}%")'
                #cmd = f'SELECT filename,tags,user_tags FROM collection where (tags LIKE "%{tag}%" OR user_tags LIKE "%{tag}%") AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%" LIMIT {count}  OFFSET {offset}'
                #cmd2 = f'SELECT count(*) FROM collection where (tags LIKE "%{tag}%" OR user_tags LIKE "%{tag}%") AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%"'
                cmd = f'SELECT filename,tags,user_tags,create_time,latitude,longitude,location,size,size_units FROM collection where {tag_cmd} AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%" LIMIT {count}  OFFSET {offset}'
                cmd2 = f'SELECT count(*) FROM collection where {tag_cmd} AND type LIKE "%photo%" and user_tags NOT LIKE "%delete%"'
        print(cmd)
        myCursor.execute(cmd)
        temp = myCursor.fetchall()
        print(f"... rows : {temp}")
        
        print(cmd2)
        myCursor.execute(cmd2)
        temp2 = myCursor.fetchall()
        print(f"... row_count : {temp2[0][0]}")

        file_list = []
        user_tag_list = []
        for t in temp:
            if t[6] is None:
                location = get_location(t[3],t[4],t[5])
            else:
                location = t[6]
            file_list.append((t[0], t[1], t[2], t[4], t[5], location,t[7],t[8]))
            for ut in t[2].split(':'):
                if ut not in user_tag_list:
                    user_tag_list.append(ut)
        conn.close()
        print(f"..file_list     : {file_list}..")
        print(f'..user_tag_list : {user_tag_list}..')
        print(f'opening {db_file}')
        conn = sqlite3.connect(db_file)
        myCursor = conn.cursor()
        today = datetime.datetime.now().strftime('%-Y-%-m-%-d')
        for ntag in user_tag_list:
            a = myCursor.execute(f'REPLACE INTO tag_table (tag,last_used) VALUES ("{ntag}","{today}")')
            #a = myCursor.execute(f'UPDATE tag_table SET last_used="{today}" WHERE tag = "{ntag}"')
            b = conn.commit()
        conn.close()

        retval = make_response()
        retval.headers.add("Access-Control-Allow-Origin", "*") 
        retval = jsonify(file_list=file_list, row_count=temp2[0][0])
        return(retval)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
