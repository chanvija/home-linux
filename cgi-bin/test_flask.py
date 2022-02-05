from flask import Flask, request, jsonify, make_response, render_template
from time import sleep
import os, json

app = Flask(__name__)

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
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return(response)
    elif ( request.method == 'POST' or request.method == "GET" ):
        retval = jsonify(log_lines=generate())
        retval.headers.add("Access-Control-Allow-Origin", "*") 
        return app.response_class(retval, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
    
