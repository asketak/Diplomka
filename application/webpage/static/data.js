var piedata = [
	{
		"label": "Unknown",
		"value": 8,
		"color": "#f30000"
	},
	{
		"label": "SatoshiDice",
		"value": 4,
		"color": "#0600f3"
	},
	{
		"label": "Bitfinex",
		"value": 2,
		"color": "#00b109"
	},
	{
		"label": "Addresses with identities",
		"value": 1,
		"color": "#67f200"
	}]

var piedata2 = [
	{
		"label": "Unknown",
		"value": 8,
		"color": "#f30000"
	},
	{
		"label": "SatoshiDice",
		"value": 4,
		"color": "#0600f3"
	},
	{
		"label": "Bitfinex",
		"value": 2,
		"color": "#00b109"
	},
	{
		"label": "Addresses with identities",
		"value": 1,
		"color": "#67f200"
	}]
	
var tabledata=[
	{
		"address": "14BzdTwZyJTWewiZdYMGafiNUxmSYm9K91",
		"distance": "7",
		"identity": "Arnodl",
		"url": "bitcointalk.com/profile=148",
		"btc": "1.37",
	},
	{
		"address": "343zdTXZyJTWewiZdYM33fiNUxmSYm3333",
		"distance": "2",
		"identity": "SlushPool",
		"url": "slushpool.com",
		"btc": "0.2",
	}
]

var distancedata=[
		{
		x: 0,
		y: 0,
		c: 0,
		size: 0
	},
	{
		x: 2,
		y: 3,
		c: 0,
		size: 500
	},
	{
		x: 30,
		y: 70,
		c: 1,
		size: 800
	},
	{
		x: 5,
		y: 2,
		c: 2,
		size: 500
	},
	{
		x: 4,
		y: 4,
		c: 3,
		size: 1000
	}
	
]

var transactionsdata = {
  "nodes": [
    {"id": "A1", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500},
    {"id": "A2", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500},
    {"id": "A3", "text": "vstupni TX", "group": 1, "value": 500, "value2": 500},
    {"id": "A", "text": "Adresa", "group": 2, "value": 500, "value2": 500},
    {"id": "B", "text": "vystupni TX", "group": 3, "value": 300, "value2": 300},
    {"id": "C", "text": "vystupni TX", "group": 3, "value": 500, "value2": 500},
    {"id": "D", "text": "vystupni TX", "group": 3, "value": 100, "value2": 100},
    {"id": "E", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50},
    {"id": "F", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50},
    {"id": "G", "text": "vystupni TX", "group": 3, "value": 50, "value2": 50}


  ],
  "links": [
    {"source": "A1", "target": "A", "value": 1},
    {"source": "A2", "target": "A", "value": 1},
    {"source": "A3", "target": "A", "value": 1},
    {"source": "A", "target": "B", "value": 1},
    {"source": "A", "target": "C", "value": 1},
    {"source": "A", "target": "D", "value": 1},
    {"source": "D", "target": "E", "value": 1},
    {"source": "D", "target": "F", "value": 1},
    {"source": "F", "target": "G", "value": 1}
  ]
}