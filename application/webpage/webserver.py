from flask import Flask, session, redirect, url_for, escape, request
import json
from pprint import pprint
from subprocess import check_output
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
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



def generateData(address):

    mock_data=""" var piedata = [ { "label": "Unknown", "value": 8, "color": "#f30000" }, { "label": "SatoshiDice", "value": 4, "color": "#0600f3" }, { "label": "Bitfinex", "value": 2, "color": "#00b109" }, { "label": "Addresses with identities", "value": 1, "color": "#67f200"
    }]
var distancedata=[ { x: 0, y: 0, c: 0, size: 0 }, { x: 2, y: 3, c: 0, size: 500 }, { x: 30, y: 70, c: 1, size: 800 }, { x: 5, y: 2, c: 2, size: 500 }, { x: 4, y: 4, c: 3, size: 1000 } ] var transactionsdata = { "nodes": [ {"id": "A1", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500}, {"id": "A2", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500}, {"id": "A3", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500}, {"id": "A", "text": "Adresa", "group": 2, "value": 500, "value2": 500}, {"id": "B", "text": "vystupni TX", "group": 3, "value": 300, "value2": 300}, {"id": "C", "text": "vystupni TX", "group": 3, "value": 500, "value2": 500}, {"id": "D", "text": "vystupni TX", "group": 3, "value": 100, "value2": 100}, {"id": "E", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50}, {"id": "F", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50}, {"id": "G", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50} 
  ], "links": [ {"source": "A1", "target": "A", "value": 1}, {"source": "A2", "target": "A", "value": 1}, {"source": "A3", "target": "A", "value": 1}, {"source": "A", "target": "B", "value": 1},
    {"source": "A", "target": "C", "value": 1}, {"source": "A", "target": "D", "value": 1}, {"source": "D", "target": "E", "value": 1}, {"source": "D", "target": "F", "value": 1},
    {"source": "F", "target": "G", "value": 1} ]

}"""

    refstring = """var tabledata=[
    {
        "address": "14BzdTwZyJTWewiZdYMGafiNUxmSYm9K91",
        "distance": "7",
        "identity": "Arnodl",
        "url": "bitcointalk.com/profile=148",
        "btc": "1.37",
    },
    {
        "address": "343zdTXZyJTWewiZdYM33fiNUxmSYm3333",
        "distance": "2",
        "identity": "SlushPool",
        "url": "slushpool.com",
        "btc": "0.2",
    }
]
"""

    tabledata_req =  """MATCH (start:Identity)-[]-(strt:Address )<-[:USES]-(o1:Output)
             -[:INPUT|OUTPUT*1..6]->(o2:Output)-[:USES]->(end:Address {address: '1AEfmTfVsWMWhnw96FiF5jpzTy57wSQRjs'}),
  p = shortestpath((o1)-[:INPUT|OUTPUT*1..6]->(o2))
  with start,p
  limit 1
  return start,strt,p"""

    r = requests.post(' http://localhost:7474/db/data/transaction/commit', json={ "statements" : [ { "statement" : tabledata_req }, { "statement" : "match (n:Address) RETURN (n) limit 1" }] })
    if(r.status_code != 200):
        return app.send_static_file("error.html")

    data = r.json()
    tabledata = r.json()['results'][0]['data'] #[0]['row'][0]
    table_data_string = "var tabledata ="
    i = 0
    for row in tabledata:
        distance = length(row['row'][2])
        url = row['row'][0]['link']
        identity = row['row'][0]['name']
        address = row['row'][1]['address']
        tabrows[i]['distance'] = distance
        tabrows[i]['url'] = url
        tabrows[i]['identity'] = identity
        tabrows[i]['address'] = address
        tabrows[i]['btc'] = 1
        i += 1
        print(address + "::::" + distance + "::::" + identity + "::::" + url + "::::" )

    table_data_string  += json.dumps(tabrows)

    text_file = open("static/data.js", "w")
    text_file.write(mock_data + table_data_string)
    text_file.close()



app.secret_key = 'L\xaf\xca\x1e(\x8dZ\xcc69\xe8\x19\x83\x80\xe9\x18\xe1L^]m\xab\x086'
app.run(threaded=True)

