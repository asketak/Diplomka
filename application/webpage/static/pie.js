	


	var pie = new d3pie("pieChart2", {
		"header": {
			"title": {
				"text": "Identified bitcoins that were sent from address",
				"fontSize": 20,
				"font": "open sans"
			}
		},
		"footer": {
			"color": "#999999",
			"fontSize": 10,
			"font": "open sans",
			"location": "bottom-left"
		},
		"size": {
			"canvasWidth": 590,
			"pieInnerRadius": "24%",
			"pieOuterRadius": "62%"
		},
		"data": {
			"sortOrder": "value-desc",
			"content": piedata2
			
		},
		"labels": {
			"outer": {
				"pieDistance": 32
			},
			"inner": {
				"hideWhenLessThanPercentage": 3
			},
			"mainLabel": {
				"fontSize": 21
			},
			"percentage": {
				"color": "#ffffff",
				"decimalPlaces": 0
			},
			"value": {
				"color": "#adadad",
				"fontSize": 21
			},
			"lines": {
				"enabled": true
			},
			"truncation": {
				"enabled": true
			}
		},
		"effects": {
		},
		"misc": {
			"gradient": {
				"enabled": true,
				"percentage": 100
			}
		}
	});	


	var pie = new d3pie("pieChart", {
		"header": {
			"title": {
				"text": "Identified bitcoins that were recieved by address",
				"fontSize": 20,
				"font": "open sans"
			}
		},
		"footer": {
			"color": "#999999",
			"fontSize": 20,
			"font": "open sans",
			"location": "bottom-left"
		},
		"size": {
			"canvasWidth": 590,
			"pieInnerRadius": "24%",
			"pieOuterRadius": "62%"
		},
		"data": {
			"sortOrder": "value-desc",
			"content": piedata
			
		},
		"labels": {
			"outer": {
				"pieDistance": 32
			},
			"inner": {
				"hideWhenLessThanPercentage": 3
			},
			"mainLabel": {
				"fontSize": 21
			},
			"percentage": {
				"color": "#ffffff",
				"decimalPlaces": 0
			},
			"value": {
				"color": "#adadad",
				"fontSize": 21
			},
			"lines": {
				"enabled": true
			},
			"truncation": {
				"enabled": true
			}
		},
		"effects": {
		},
		"misc": {
			"gradient": {
				"enabled": true,
				"percentage": 100
			}
		}
	});