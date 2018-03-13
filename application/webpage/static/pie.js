	


	var pie = new d3pie("pieChart", {
		"header": {
			"title": {
				"text": "Sources of BTC",
				"fontSize": 24,
				"font": "open sans"
			},
			"subtitle": {
				"text": "For bitcoin address: XXXYUYY",
				"color": "#999999",
				"fontSize": 12,
				"font": "open sans"
			},
			"titleSubtitlePadding": 9
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
				"fontSize": 11
			},
			"percentage": {
				"color": "#ffffff",
				"decimalPlaces": 0
			},
			"value": {
				"color": "#adadad",
				"fontSize": 11
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
		},
		callbacks: {
			onClickSegment: function(a) {
				alert("Segment clicked! See the console for all data passed to the click handler.");
				console.log(a);
			}
		}
	});