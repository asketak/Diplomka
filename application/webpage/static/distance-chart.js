console.log("CHAR")
var height = 400;
var width = 600;
var margin = 80;
var data =[];
for(var i = 0; i < 42; i++) {
	data.push({
    	x: Math.random() * 400,
        y: Math.random() * 100,
        c: Math.round(Math.random() * 5),
        size: Math.random() * 200,
        });
}

console.log(data)
data = distancedata
console.log(data)
var labelX = 'Distance from address';
var labelY = 'Certainty of ownership';
var svg = d3v3.select('.chart')
                    .append('svg')
                    .attr('class', 'chart')
                    .attr("width", width + margin + margin)
                    .attr("height", height + margin + margin)
                    .append("g")
                    .attr("transform", "translate(" + margin + "," + margin + ")");
                    
var x = d3v3.scale.linear()
					            .domain([d3v3.min(data, function (d) { return d.x; }), d3v3.max(data, function (d) { return d.x; })])
					            .range([0, width]);

var y = d3v3.scale.linear()
					            .domain([d3v3.min(data, function (d) { return d.y; }), d3v3.max(data, function (d) { return d.y; })])
					            .range([height, 0]);

var scale = d3v3.scale.sqrt()
					            .domain([d3v3.min(data, function (d) { return d.size; }), d3v3.max(data, function (d) { return d.size; })])
					            .range([1, 20]);

var opacity = d3v3.scale.sqrt()
					            .domain([d3v3.min(data, function (d) { return d.size; }), d3v3.max(data, function (d) { return d.size; })])
					            .range([1, .5]);
                                
var color = d3v3.scale.category10();

var xAxis = d3v3.svg.axis().scale(x);
 var yAxis = d3v3.svg.axis().scale(y).orient("left");
 
  svg.append("g")
					        .attr("class", "y axis")
					        .call(yAxis)
					        .append("text")
						        .attr("x", -margin/2)
						        .attr("y", -margin/2)
						        .attr("dy", ".71em")
						        .style("text-anchor", "end")
						        .text(labelY);
                          // x axis and label
                          svg.append("g")
                              .attr("class", "x axis")
                              .attr("transform", "translate(0," + height + ")")
                              .call(xAxis)
                              .append("text")
                                  .attr("x", width + 20)
                                  .attr("y", margin - 10)
                                  .attr("dy", ".71em")
                                  .style("text-anchor", "end")
                                  .text(labelX);
 
svg.selectAll("circle")
                              .data(data)
                              .enter()
                              .insert("circle")
                              .attr("cx", width / 2)
                              .attr("cy", height / 2)
                              .attr("opacity", function (d) { return opacity(d.size); })
                              .attr("r", function (d) { return scale(d.size); })
                              .style("fill", function (d) { return color(d.c); })
                              .on('mouseover', function (d, i) {
                                  fade(d.c, .1);
                              })
                             .on('mouseout', function (d, i) {
                                 fadeOut();
                             })
                             .transition()
                            .delay(function (d, i) { return x(d.x) - y(d.y); })
                            .duration(500)
                            .attr("cx", function (d) { return x(d.x); })
                            .attr("cy", function (d) { return y(d.y); })
                            .ease("bounce");
                             
                             
function fade(c, opacity) {
                              svg.selectAll("circle")
                                  .filter(function (d) {
                                      return d.c != c;
                                  })
                                .transition()
                                 .style("opacity", opacity);
                          }

                          function fadeOut() {
                              svg.selectAll("circle")
                              .transition()
                                 .style("opacity", function (d) { opacity(d.size); });
                          }