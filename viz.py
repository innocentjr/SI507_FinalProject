    # Import statements necessary
from flask import Flask, render_template
from flask import Flask, render_template
from flask_script import Manager
import requests
import json
from random import *

# Set up application
app = Flask(__name__)

#manager = Manager(app)

# Routes
@app.route('/')
def grab_data():
    with open('viz_data.json','r') as f:
        loading = json.loads(f.read())
        f.close()
    keys = []
    for each in loading.keys():
        keys.append(each)
    data1 = loading[keys[0]]
    data2 = loading[keys[1]]
    #data1 = json.dumps(data1)
    #data2 = json.dumps(data2)
    # TODO: Add some code here that processes flickr_data in some way to get what you nested
    # TODO: Edit the invocation to render_template to send the data you need
    return render_template('pfsviz.html', data1 = data1, data2 = data2 )

#comment
if __name__ == '__main__':
    app.run() # Runs the flask server in a special way that makes it nice to debug
