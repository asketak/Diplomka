from __future__ import print_function
from flask import Flask, session, redirect, url_for, escape, request
import json
from pprint import pprint
from subprocess import check_output
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
import sys
import requests

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

app = Flask(__name__)

@app.route('/')
@nocache
def root():
    return app.send_static_file("index.html")

@app.route('/<path:path>', methods=['GET'])
@nocache
def filea(path):
    return app.send_static_file(path)

@app.route('/<path:path>', methods=['POST'])
@nocache
def static_file(path):
    address = request.form['searched_address']
    generateData(address);
    return app.send_static_file(path)

def generateJson(rec,send):
    tabrows = []

    for row in rec:
        distance = len(row['row'][2])/2/2 
        url = row['row'][0]['link']
        identity = row['row'][0]['name']
        address = row['row'][1]['address']
        outgoing = row['row'][2][0]['value']
        tabrow = {}
        tabrow['distance'] = distance
        tabrow['url'] = url
        tabrow['identity'] = identity
        tabrow['address'] = address
        tabrow['btc'] = outgoing
        tabrows.append(tabrow)

    for row in send:
        distance = -1*len(row['row'][2])/2/2 
        url = row['row'][0]['link']
        identity = row['row'][0]['name']
        address = row['row'][1]['address']
        outgoing = row['row'][2][0]['value']
        tabrow = {}
        tabrow['distance'] = distance
        tabrow['url'] = url
        tabrow['identity'] = identity
        tabrow['address'] = address
        tabrow['btc'] = outgoing
        tabrows.append(tabrow)

    return tabrows


def parsetable(data):
    send = data['results'][0]['data'] 
    rec = data['results'][1]['data'] 
    table_data_string = generateJson(rec,send) 
    return table_data_string


def parserecieved(data):
    rec = data['results'][2]['data'][0]['row'][0]
    return rec

def parsesent(data):
    sent = data['results'][3]['data'][0]['row'][0]
    return sent
    

def parsedist(data):
    sent = data['results'][0]['data'] 
    rec = data['results'][1]['data'] 
    for row in rec:
        distance = len(row['row'][2])/2/2 
        pagerank = row['row'][0]['pagerank']
        identity = row['row'][0]['name']
        address = row['row'][1]['address']
        outgoing = row['row'][2][0]['value']
        tabrow = {}
        tabrow['distance'] = distance
        tabrow['url'] = url
        tabrow['identity'] = identity
        tabrow['address'] = address
        tabrow['btc'] = outgoing
        tabrows.append(tabrow)

    for row in send:
        distance = -1*len(row['row'][2])/2/2 
        pagerank = row['row'][0]['pagerank']
        size = row['row'][0]['value']
        address = row['row'][1]['address']
        outgoing = row['row'][2][0]['value']
        tabrow = {}
        tabrow['distance'] = distance
        tabrow['url'] = url
        tabrow['identity'] = identity
        tabrow['address'] = address
        tabrow['btc'] = outgoing
        tabrows.append(tabrow)

    return tabrows 




def compute_recieved(tabrows,recieved):
    ret = "var piedata = "
    rectot = 0
    js = []
    for row in tabrows:
        if row['distance'] >0:
            x = {}
            x['label'] = row['identity']
            x['value'] = row['btc']
            rectot+=row['btc']
            x['color'] = '#0600f3'
            js.append(x)

    x = {}
    x['label'] = 'Unknown'
    x['value'] = recieved -rectot
    x['color'] = '#0600f3'
    js.append(x)
    ret += json.dumps(js)
    return ret

def compute_sent(tabrows,recieved):
    ret = "var piedata2 = "
    rectot = 0
    js = []
    for row in tabrows:
        if row['distance'] <0:
            x = {}
            x['label'] = row['identity']
            x['value'] = row['btc']
            rectot+=row['btc']
            x['color'] = '#0600f3'
            js.append(x)

    x = {}
    x['label'] = 'Unknown'
    x['value'] = recieved -rectot
    x['color'] = '#0600f3'
    js.append(x)
    ret += json.dumps(js)
    return ret


def generateData(address):


    distance_graph_req=""" 
    var distancedata=[ { x: 0, y: 0, c: 0, size: 0 }, { x: 2, y: 3, c: 0, size: 500 }, { x: 30, y: 70, c: 1, size: 800 }, { x: 5, y: 2, c: 2, size: 500 }, { x: 4, y: 4, c: 3, size: 1000 } ] 
    """

    tx_graph_req = """
    var transactionsdata = { "nodes": [ {"id": "A1", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500}, {"id": "A2", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500}, {"id": "A3", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500}, {"id": "A", "text": "Adresa", "group": 2, "value": 500, "value2": 500}, {"id": "B", "text": "vystupni TX", "group": 3, "value": 300, "value2": 300}, {"id": "C", "text": "vystupni TX", "group": 3, "value": 500, "value2": 500}, {"id": "D", "text": "vystupni TX", "group": 3, "value": 100, "value2": 100}, {"id": "E", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50}, {"id": "F", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50}, {"id": "G", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50} 
  ], "links": [ {"source": "A1", "target": "A", "value": 1}, {"source": "A2", "target": "A", "value": 1}, {"source": "A3", "target": "A", "value": 1}, {"source": "A", "target": "B", "value": 1},
    {"source": "A", "target": "C", "value": 1}, {"source": "A", "target": "D", "value": 1}, {"source": "D", "target": "E", "value": 1}, {"source": "D", "target": "F", "value": 1},
    {"source": "F", "target": "G", "value": 1} ] }

    """

    mock_data = ""

    tabledata_rec_req =  """MATCH (start:Identity)-[]-(strt:Address )<-[:USES]-(o1:Output)
    -[:INPUT|OUTPUT*1..6]->(o2:Output)-[:USES]->(end:Address {address: '""" + address+ """'}),
    p = shortestpath((o1)-[:INPUT|OUTPUT*1..6]->(o2))
    with start,strt,p
    limit 2
    return start,strt,p"""

    tabledata_send_req = """MATCH (end:Address {address: '""" + address+ """'} )<-[:USES]-(o1:Output)
    -[:INPUT|OUTPUT*1..6]->(o2:Output)-[:USES]->(strt:Address)-[]-(start:Identity),
    p = shortestpath((o1)-[:INPUT|OUTPUT*1..6]->(o2))
    with start,strt,p
    limit 2
    return start,strt,p"""

    total_recieved_req =  """MATCH (a:Address {address: '""" + address + """' })<-[:USES]-(o),
          (o)-[r:INPUT|OUTPUT]-(t)
        WITH a, t,
        CASE type(r) WHEN "OUTPUT" THEN sum(o.value) ELSE -sum(o.value) END AS value
        WITH a, t,  sum(value) AS value
            WHERE value > 0
            RETURN sum(value);"""

    total_sent_req =  """MATCH (a:Address {address: '""" + address + """' })<-[:USES]-(o)
            WHERE (o)-[:INPUT]->()
            RETURN sum(o.value)"""



    r = requests.post(' http://localhost:7474/db/data/transaction/commit',
     json={ "statements" : [{ "statement" : tabledata_send_req }
    , { "statement" : tabledata_rec_req }
    , { "statement" : total_recieved_req }
    , { "statement" : total_sent_req }
     ]
      })


    if(r.status_code != 200):
        return app.send_static_file("error.html")

    data = r.json() 
    print("==============")
    print(data)
    print("==============")

    # compute distance table
    tabrows = parsetable(data)
    table_data_string = "var tabledata =" 
    table_data_string += json.dumps(tabrows)

    # compute pie charts
    recieved = parserecieved(data)
    sent = parsesent(data)

    pie_recieved_string = compute_recieved(tabrows,recieved)
    pie_sent_string = compute_sent(tabrows, sent)
    print(pie_recieved_string)
    print(pie_sent_string)


    text_file = open("static/data.js", "w")
    text_file.write(mock_data + table_data_string + "\n" + pie_recieved_string + "\n" + pie_sent_string)
    text_file.close()



app.secret_key = 'L\xaf\xca\x1e(\x8dZ\xcc69\xe8\x19\x83\x80\xe9\x18\xe1L^]m\xab\x086'
app.run(threaded=True)
