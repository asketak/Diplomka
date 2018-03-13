from flask import Flask, session, redirect, url_for, escape, request
import json
from pprint import pprint
from subprocess import check_output
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime

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
    generateJson(address);
    return app.send_static_file(path)



def generateJson(address):
    return
    params = "searchrawtransactions"
    info = check_output(["./bitcoin-cli",params,unicode(address).encode('utf8') ,"1","0","10000"])
    text_file = open("info.txt", "w")
    text_file.write(info)
    text_file.close()

    with open('info.txt') as data_file:    
        data = json.load(data_file)
        tx_count = 0
        jsonString = """ {"nodes": [ """
        jsonString += "  {\"id\":0, \"tx\": \"https://blockchain.info/address/" + address + "\", \"size\":450  } "

        for transaction in data:
            tx_size = 0
            out_transaction_flag = 0
            for out in transaction[u'vout']:
                tx_size+= out[u'value']
                if address in out[u'scriptPubKey'][u'addresses']:
                    out_transaction_flag = 1

            jsonString += ','
            tx_count += 1
            txid = (transaction[u'txid'])
            jsonString += "  {\"id\":"  + str(tx_count) + ", \"tx\": \"https://blockchain.info/tx/" + str(txid) +  "\", \"size\":"  + str(tx_size) + ",  \"out\":"  + str(out_transaction_flag) +"  } "

        jsonString +=  """ ], "links": [ """
        for x in xrange(1,tx_count+1):
            if x > 1:
                jsonString += ',' 
            jsonString +=   """  {"source": 0, "target": """ + str(x) + "}"
        jsonString += "  ] }"

    text_file = open("static/miserables.json", "w")
    text_file.write(jsonString)
    text_file.close()



app.secret_key = 'L\xaf\xca\x1e(\x8dZ\xcc69\xe8\x19\x83\x80\xe9\x18\xe1L^]m\xab\x086'
app.run(threaded=True)

