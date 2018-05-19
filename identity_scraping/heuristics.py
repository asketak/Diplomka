from __future__ import print_function
import json
from pprint import pprint
from subprocess import check_output
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
import sys
import requests

heur_init_req = """MATCH (first:Address ) 
set first.userid = ID(first)
"""

heur1_req =  """MATCH (first:Address )<-[:USES]-(i1:Output)
-[:INPUT]-(tx:transaction)<-[:INPUT]-(i2:Output)-[:USES]-(second:Address),
where not first.address != second.address 
set first.userid = min([first.userid,second.userid])
set second.userid = min([first.userid,second.userid])
"""

twoOutputTx_req =  """MATCH (t:transaction)-[:OUTPUT]->(o:Output) 
WITH t,count(o) as rels
WHERE rels = 2
RETURN t"""

r = requests.post(' http://localhost:7474/db/data/transaction/commit',
   json={ "statements" : [{ "statement" : heur_init_req } ] })

if(r.status_code != 200):
    print("Error during heuristics setup")
    sys.exit()

    r = requests.post(' http://localhost:7474/db/data/transaction/commit',
       json={ "statements" : [{ "statement" : twoOutputTx_req } ] })

    if(r.status_code != 200):
        print("Error during two output tx search")
        sys.exit()
        txs = r.json() 
        txs = txs['results'][0]['data']
        for tx in txs:
            txid = tx['row'][0]['hash']
            total_recieved_req =  """
            MATCH (t:transaction {hash: '""" + txid + """' })<-[:OUTPUT]-(o2:Output),
            MATCH (t:transaction {hash: '""" + txid + """' })<-[:OUTPUT]-(o1:Output),
            where not o1.hash != o2.hash
            return o1,o2
            """ 
            r = requests.post(' http://localhost:7474/db/data/transaction/commit',
               json={ "statements" : [{ "statement" : heur2_req } ] })

            out = r.json() 
            first  = out['results'][0]['data']['row'][0]['hash']
            second = out['results'][0]['data']['row'][1]['hash']

            first_req =  """
            MATCH (o1:Output {hash: '""" + first + """' })<-[:OUTPUT|INPUT]-(tx:transaction),
            return tx
            """ 
            r = requests.post(' http://localhost:7474/db/data/transaction/commit',
               json={ "statements" : [{ "statement" : heur2_req } ] })

            find_earliest_block()

            second_req =  """
            MATCH (o1:Output {hash: '""" + second + """' })<-[:OUTPUT|INPUT]-(tx:transaction),
            return tx
            """ 

            r = requests.post(' http://localhost:7474/db/data/transaction/commit',
               json={ "statements" : [{ "statement" : heur2_req } ] })

