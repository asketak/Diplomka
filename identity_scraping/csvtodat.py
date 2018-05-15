import json
import sys
import os
from pprint import pprint
from tqdm import *
import time
from datetime import datetime, timedelta
import subprocess

os.path.isfile(addresses.csv)
os.path.isfile(transactions.csv)
os.path.isfile(outputs.csv)
os.path.isfile(identities.csv)
os.path.isfile(outputs-transactions.csv)
os.path.isfile(outputs-addresses.csv)

importcomm = "neo4j-import --into ./data/blockchain.db "

--nodes:Address addresses.csv
--nodes:Transaction transactions.csv \
--nodes:Outputs outputs.csv \
--relationships:Oinput outputs-transactions.csv
--relationships:Owns outputs-addresses.csv
--relationships:Identity identities.csv

addresses = subprocess.getoutput(importcomm + addimport)
transactions = subprocess.getoutput(importcomm + tranimport)
outputs = subprocess.getoutput(importcomm + outimport)
oinput = subprocess.getoutput(importcomm + outtrans)
identity = subprocess.getoutput(importcomm + outaddd)
identity = subprocess.getoutput(importcomm + identities)
