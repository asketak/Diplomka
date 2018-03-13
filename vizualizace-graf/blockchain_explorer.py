from flask import Flask, session, redirect, url_for, escape, request
import json
from pprint import pprint
from subprocess import check_output
app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return app.send_static_file('index.html')
    if request.method == 'POST':
        generateJson(request.form.get('address'));
        return app.send_static_file('index.html')


def generateJson(address):
    params = ""
    info = check_output(["/root/velke/neo4j-community-3.3.2/bin/cypher-shell",params,unicode(address).encode('utf8') ,"1","0","10000"])


    text_file = open("static/miserables.json", "w")
    text_file.write(jsonString)
    text_file.close()



app.secret_key = 'L\xaf\xca\x1e(\x8dZ\xcc69\xe8\x19\x83\x80\xe9\x18\xe1L^]m\xab\x086'
app.run(threaded=True)















