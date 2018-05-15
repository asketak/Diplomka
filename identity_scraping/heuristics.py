
    distance_graph_req=""" 
    var distancedata=[ { x: 0, y: 0, c: 0, size: 0 }, { x: 2, y: 3, c: 0, size: 500 }, { x: 30, y: 70, c: 1, size: 800 }, { x: 5, y: 2, c: 2, size: 500 }, { x: 4, y: 4, c: 3, size: 1000 } ] 
    """

    tx_graph_req = """
    var transactionsdata = { "nodes": [ {"id": "A1", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500}, {"id": "A2", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500}, {"id": "A3", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500}, {"id": "A", "text": "Adresa", "group": 2, "value": 500, "value2": 500}, {"id": "B", "text": "vystupni TX", "group": 3, "value": 300, "value2": 300}, {"id": "C", "text": "vystupni TX", "group": 3, "value": 500, "value2": 500}, {"id": "D", "text": "vystupni TX", "group": 3, "value": 100, "value2": 100}, {"id": "E", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50}, {"id": "F", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50}, {"id": "G", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50} 
  ], "links": [ {"source": "A1", "target": "A", "value": 1}, {"source": "A2", "target": "A", "value": 1}, {"source": "A3", "target": "A", "value": 1}, {"source": "A", "target": "B", "value": 1},
    {"source": "A", "target": "C", "value": 1}, {"source": "A", "target": "D", "value": 1}, {"source": "D", "target": "E", "value": 1}, {"source": "D", "target": "F", "value": 1},
    {"source": "F", "target": "G", "value": 1} ] }

    """

    mock_data = ""

    tabledata_rec_req =  """MATCH (start:Identity)-[]-(strt:Address )<-[:USES]-(o1:Output)
    -[:INPUT|OUTPUT*1..6]->(o2:Output)-[:USES]->(end:Address {address: '""" + address+ """'}),
    p = shortestpath((o1)-[:INPUT|OUTPUT*1..6]->(o2))
    with start,strt,p
    limit 2
    return start,strt,p"""

    tabledata_send_req = """MATCH (end:Address {address: '""" + address+ """'} )<-[:USES]-(o1:Output)
    -[:INPUT|OUTPUT*1..6]->(o2:Output)-[:USES]->(strt:Address)-[]-(start:Identity),
    p = shortestpath((o1)-[:INPUT|OUTPUT*1..6]->(o2))
    with start,strt,p
    limit 2
    return start,strt,p"""

    total_recieved_req =  """MATCH (a:Address {address: '""" + address + """' })<-[:USES]-(o),
          (o)-[r:INPUT|OUTPUT]-(t)
        WITH a, t,
        CASE type(r) WHEN "OUTPUT" THEN sum(o.value) ELSE -sum(o.value) END AS value
        WITH a, t,  sum(value) AS value
            WHERE value > 0
            RETURN sum(value);"""

    total_sent_req =  """MATCH (a:Address {address: '""" + address + """' })<-[:USES]-(o)
            WHERE (o)-[:INPUT]->()
            RETURN sum(o.value)"""



    r = requests.post(' http://localhost:7474/db/data/transaction/commit',
     json={ "statements" : [{ "statement" : tabledata_send_req }
    , { "statement" : tabledata_rec_req }
    , { "statement" : total_recieved_req }
    , { "statement" : total_sent_req }
     ]
      })


    if(r.status_code != 200):
        return app.send_static_file("error.html")

    data = r.json() 
    print("==============")
    print(data)
    print("==============")

    # compute distance table
    tabrows = parsetable(data)
    table_data_string = "var tabledata =" 
    table_data_string += json.dumps(tabrows)

    # compute pie charts
    recieved = parserecieved(data)
    sent = parsesent(data)

    pie_recieved_string = compute_recieved(tabrows,recieved)
    pie_sent_string = compute_sent(tabrows, sent)
    print(pie_recieved_string)
    print(pie_sent_string)


    text_file = open("static/data.js", "w")
    text_file.write(mock_data + table_data_string + "\n" + pie_recieved_string + "\n" + pie_sent_string)
    text_file.close()

