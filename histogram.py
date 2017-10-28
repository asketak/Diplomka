import json
import sys
from pprint import pprint
from subprocess import check_output
from tqdm import *
import time

startblock = 480000
blocks = 2000


output = {}

for block_height in tqdm(xrange(startblock,startblock + blocks)):
    try:
        params = "getblockhash"
        blockhash = check_output(["./bitcoin-cli",params,unicode(block_height).encode('utf8')])

        params = "getblock"
        block_info = check_output(["./bitcoin-cli",params,unicode(blockhash).encode('utf8')])
        block_data = json.loads(block_info)
    except Exception as e:
        continue

    for index,tx_hash in enumerate(block_data['tx']):
        # print(str(index) + "," + tx_hash)
        # sys.stdout.flush()
        try:
            params = "getrawtransaction"
            tx_info = check_output(["./bitcoin-cli",params,unicode(tx_hash).encode('utf8')])
            tx_info = tx_info[:-1]
            params = "decoderawtransaction"
            tx_info = check_output(["./bitcoin-cli",params,unicode(tx_info).encode('utf8')])
            tx_data = json.loads(tx_info)
            for out_data in tx_data[u'vout']:
                if out_data[u'value'] in output:
                    output[out_data[u'value']] += 1
                else:
                    output[out_data[u'value']] = 1
        except Exception as e:
            continue

file = open("superhistogram.txt", 'w' )
for value in output.keys():
    file.write(str(output[value]) + "," + str(value) +  "\n")
