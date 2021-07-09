from flask import Flask, request, jsonify, make_response
import sqlite3
import os
import json

app = Flask(__name__)

db_file = "/usr/local/var/www/home-linux-www/html/cdj-album.db"

@app.route('/test_db',methods = ['POST', 'OPTIONS'])
def hello_world():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        os.system('touch /tmp/abcd')
        return(response)
    elif request.method == 'POST':
        new_tag = request.form['new_tag']
        filename = request.form['filename']
        if True:
            conn = sqlite3.connect(db_file)
            myCursor = conn.cursor()
            myCursor.execute('SELECT tags FROM collection where filename = "' + filename + '"')
            temp = myCursor.fetchall()
            for t in temp[0][0].split(","):
                new_tag =  new_tag + "," + str(t) if t else new_tag
            myCursor.execute('UPDATE collection SET tags="' + new_tag + '" WHERE filename = "' + filename + '"')
            conn.commit()
            myCursor.execute('SELECT tags FROM collection where filename = "' + filename + '"')
            new_current_tags = myCursor.fetchall()
            conn.close()
            retval = f"Old tag : {temp[0]}  Updated tag : {str(new_current_tags[0])}"
            retval.headers.add("Access-Control-Allow-Origin", "*") 
            return(retval)
        else:
            return(filename)
            
@app.route('/get_row',methods = ['POST', 'OPTIONS'])
def get_row():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        os.system('touch /tmp/abcd')
        return(response)
    elif request.method == 'POST':
        data = request.get_json()        
        tag = data['tag']
        count = data['count']
        offset = data['offset']
        if True:
            conn = sqlite3.connect(db_file)
            myCursor = conn.cursor()
            if tag == "today":
                cmd = f'SELECT filename FROM collection WHERE day = strftime("%d","now", "localtime") AND month = strftime("%m","now", "localtime") AND type LIKE "%photo%" ORDER by year,filename LIMIT {count} OFFSET {offset}'
            else:
                cmd = f'SELECT filename FROM collection where tags LIKE "%{tag}%" LIMIT {count}  OFFSET {offset}'
            myCursor.execute(cmd)
            temp = myCursor.fetchall()
            file_list = []
            for t in temp:
                file_list.append(t[0])
            conn.close()
            print(file_list)
            retval = jsonify(file_list)
            retval.headers.add("Access-Control-Allow-Origin", "*") 
            print(f".... {retval}...")
            return(retval)
        else:
            retval = filename
            retval.headers.add("Access-Control-Allow-Origin", "*") 
            return(retval)

#app.add_url_rule('/test_db', 'hello_world', hello_world)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
    
