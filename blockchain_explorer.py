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















