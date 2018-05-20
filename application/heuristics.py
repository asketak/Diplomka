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

    r = requests.post(' http://localhost:7474/db/data/transaction/commit',
       json={ "statements" : [{ "statement" : twoOutputTx_req } ] })

    if(r.status_code != 200):
        txs = r.json() 
        txs = txs['results'][0]['data']
        for tx in txs:
            txid = tx['row'][0]['hash']
            get2out_req =  """
            MATCH (b:block)-[]-(t:transaction {hash: '""" + txid + """' })<-[:OUTPUT]-(o2:Output)-(first:Address )<-[:USES]-,
            MATCH (b:block)-[]-(t:transaction {hash: '""" + txid + """' })<-[:OUTPUT]-(o1:Output)-(second:Address )<-[:USES]-,
            MATCH (b:block)-[]-(t:transaction {hash: '""" + txid + """' })<-[:INPUT]-(o1:Output)-(in:Address )<-[:USES]-,
            where not o1.hash != o2.hash
            return first,second,b,in
            """ 
            r = requests.post(' http://localhost:7474/db/data/transaction/commit',
               json={ "statements" : [{ "statement" : get2out_req} ] })

            out = r.json() 
            firstA  = out['results'][0]['data']['row'][1]['address']
            secondA = out['results'][0]['data']['row'][2]['address']
            blockh = out['results'][0]['data']['row'][3]['height']
            inputUser = out['results'][0]['data']['row'][4]['userid']

            first_req =  """
            MATCH (first:Address {address: '""" + firstA + """' }  )<-[:USES]-(o1:Output)<-[:OUTPUT|INPUT]-(tx:transaction)-[]-(b:block),
            return min(b:height)
            """ 

            sec_req =  """
            MATCH (first:Address {address: '""" + secondA + """' }  )<-[:USES]-(o1:Output)<-[:OUTPUT|INPUT]-(tx:transaction)-[]-(b:block),
            return min(b:height)
            """ 

            r = requests.post(' http://localhost:7474/db/data/transaction/commit',
               json={ "statements" : [{ "statement" : first_req } ] })
            dat = r.json()
            time1 = dat['results'][0]['data']['row'][0]

            r = requests.post(' http://localhost:7474/db/data/transaction/commit',
               json={ "statements" : [{ "statement" : sec_req } ] })
            dat = r.json()
            time2 = dat['results'][0]['data']['row'][0]

            flag = False
            rewrite = firstA

            if (time1 == blockh and time2 < blockh):
                rewrite = firstA
                flag = True

            if (time2 == blockh and time1 < blockh):
                rewrite = secondA
                flag = True

            if flag:
                heur2_up =  """
                MATCH (first:Address {address: '""" + rewrite + """' },
                set first.userid = '""" + inputUser+ """'
                return first
                """ 
                r = requests.post(' http://localhost:7474/db/data/transaction/commit',
                   json={ "statements" : [{ "statement" : heur2_up } ] })
