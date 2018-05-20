import json
import sys
from pprint import pprint
from subprocess import check_output
from tqdm import *
import time
from datetime import datetime, timedelta

startblock = 1
blocks = 515000
# current_block_date = datetime(2017,10,15)

# output = []
file1 = open("addresses.csv", 'w' )
file2 = open("transactions.csv", 'w' )
file3 = open("outputs.csv", 'w' )
file4 = open("outputs-transactions.csv", 'w' )
file5 = open("outputs-addresses.csv", 'w' )
file1.write("address" +  "\n")
file2.write("transaction,block"  "\n")
file3.write("output,val" +  "\n")
file4.write("output,transaction" +  "\n")
file5.write("output,address" +  "\n")

for block_height in tqdm(xrange(startblock,startblock + blocks)):
    # current_block_date += timedelta(seconds=570) # 9 a pul minuty
    try:
        params = "getblockhash"
        blockhash = check_output(["bitcoin-cli",params,unicode(block_height).encode('utf8')])

        params = "getblock"
        block_info = check_output(["bitcoin-cli",params,unicode(blockhash).encode('utf8')])
        block_data = json.loads(block_info)
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        continue

    for index,tx_hash in enumerate(block_data['tx']):
        try:
            params = "getrawtransaction"
            tx_info = check_output(["bitcoin-cli",params,unicode(tx_hash).encode('utf8')])
            tx_info = tx_info[:-1]
            params = "decoderawtransaction"
            tx_info = check_output(["bitcoin-cli",params,unicode(tx_info).encode('utf8')])
            tx_data = json.loads(tx_info + "," + block_height)
            file2.write(str(tx_hash) + "," + block_height +  "\n")
            for out_data in tx_data[u'vout']:
                val = out_data[u'value']
                address = out_data[u'address']
                outhash = out_data[u'n']
                # output.append(tup)
                file1.write(str(address) +  "\n")
                file3.write(str(outhash) + "," + str(val) +  "\n")
                file4.write(str(outhash) + "," + str(tx_hash) +  "\n")
                file5.write(str(outhash) + "," + str(address) +  "\n")
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            continue

