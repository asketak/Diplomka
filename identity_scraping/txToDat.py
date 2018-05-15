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
file = open("dblast.txt", 'w' )

for block_height in tqdm(xrange(startblock,startblock + blocks)):
    # current_block_date += timedelta(seconds=570) # 9 a pul minuty
    try:
        params = "getblockhash"
        blockhash = check_output(["./bitcoin-cli",params,unicode(block_height).encode('utf8')])

        params = "getblock"
        block_info = check_output(["./bitcoin-cli",params,unicode(blockhash).encode('utf8')])
        block_data = json.loads(block_info)
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        continue

    for index,tx_hash in enumerate(block_data['tx']):
        try:
            params = "getrawtransaction"
            tx_info = check_output(["./bitcoin-cli",params,unicode(tx_hash).encode('utf8')])
            tx_info = tx_info[:-1]
            params = "decoderawtransaction"
            tx_info = check_output(["./bitcoin-cli",params,unicode(tx_info).encode('utf8')])
            tx_data = json.loads(tx_info)
            for out_data in tx_data[u'vout']:
                    tup = (tx_hash , out_data[u'value'])
                    # output.append(tup)
                    file.write(current_block_date.strftime("%Y-%m-%d") + "," + str(tx_hash) + "," + str(out_data[u'value']) +  "\n")
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            continue

