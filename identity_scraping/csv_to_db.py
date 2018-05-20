import json
import sys
import os
from pprint import pprint
import time
from datetime import datetime, timedelta
import subprocess

add = "addresses.csv"
trans = "transactions.csv"
outputs = "outputs.csv"
ident = "identities.csv"
outtran = "outputs-transactions.csv"
outadd = "outputs-addresses.csv"
blockdb = "./data/blockchain.db"

importcomm = "neo4j-import --into " + blockdb
addimport = "--nodes:Address "+ add
tranimport = "--nodes:Transaction "+ trans
outimport = "--nodes:Outputs "+ outputs
outtrans = "--relationships:Oinput "+ ident
outaddd = "--relationships:Owns " + outtran
identities = "--relationships:Identity " + ident
okflag = True

def checkout(output, name):
    if "IMPORT DONE" in output:
        print(name+ " Import complete")
    else:
        print(name+ " Import ERROR")
        print(output)
        okflag = False
 
    

if os.path.isfile(add) and os.path.isfile(trans) and os.path.isfile(outputs) and os.path.isfile(ident) and os.path.isfile(outtran) and os.path.isfile(outadd):
    out = subprocess.getoutput(importcomm + addimport)
    checkout(out,"Address")
    out = subprocess.getoutput(importcomm + tranimport)
    checkout(out,"Transaction")
    out = subprocess.getoutput(importcomm + outimport)
    checkout(out,"Outputs")
    out = subprocess.getoutput(importcomm + outtrans)
    checkout(out,"Outputs-transactions relation")
    out = subprocess.getoutput(importcomm + outaddd)
    checkout(out,"Outputs-addresses relation")
    out = subprocess.getoutput(importcomm + identities)
    checkout(out,"Address-identities relation")
    if okflag:
        print("Import completed Succesfully")
    else:
        print("Import failed")



