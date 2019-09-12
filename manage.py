from flask import Flask
#flask更简单一个文件即可!
app = Flask(__name__)
from test import main
import json
import requests
from flask import Flask,request
@app.route('/',methods=['GET','POST'])

def main1():

    return json.dumps(main(request.form['pic']))



if __name__ == '__main__':

    app.run(debug=True, threaded=True, host='0.0.0.0', port=5080)