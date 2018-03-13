    function f2 () {
      var maxNodeSize = 50;
      var margin = {top: 30, right: 20, bottom: 30, left: 50},
      width = 900 - margin.left - margin.right,
      height = 600 - margin.top - margin.bottom;

  // data1 = [{"label":"A", "value":1}]; 
  // data2 = [{"label":"A", "value":1},{"label":"2", "value":1}]; 
  // data3 = [{"label":"A", "value":1},{"label":"2", "value":1},{"label":"3", "value":1}]; 
  // data4 = [{"label":"A", "value":1},{"label":"2", "value":1},{"label":"3", "value":1},{"label":"4", "value":1}]; 
  // data5 = [{"label":"A", "value":1},{"label":"2", "value":1},{"label":"3", "value":1},{"label":"4", "value":1},{"label":"5", "value":1}]; 

  var pie = d3.pie()
  .sort(null)
  .value(function(d) { return d.value; });


  var svg = d3.select("#area2")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var color = d3.scaleOrdinal(d3.schemeCategory10);

  var simulation = d3.forceSimulation()
  .force("link", d3.forceLink().id(function(d) { return d.id ; }).strength(2))
  .force("charge", d3.forceManyBody().strength(function(d) { return -5000 * 3/d.group; }))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("y", d3.forceY(0))
  .force("x", d3.forceX().x(0).strength(function(d) { return  1/(d.group) * 4.50 ; }));

      function handleMouseOver(d, i) {  // Add interactivity

        var myid = d.id;
        var mygroup = d.group;
        var arcBorder = d3.arc()
        .outerRadius(function (d) {
          return (Math.pow(d.data.size,1/4)*6+14);
        })
        .innerRadius(function (d) {
          return (Math.pow(d.data.size,1/4)*6+6);
        });

        // d3.select(this).append('text');
        d3.selectAll(".arc").append("path")
        .attr("class", "highlight")
        .attr("fill", function (d) {
          if (myid == d.data.nodegroup) {
            return "lime";
          }
          return "cyan";
        })
        .attr("d", arcBorder)
        .style("opacity", function (d) {
          var match1 =1;
          var match2 =1;
          for (var i = 0; i < d.data.nodegroup.length; i++) {
            for (var j = 0; j < myid.length; j++) {
              if ( d.data.nodegroup.indexOf(myid[j]) < 0) {
                match1 =0;
              } 
              if ( myid.indexOf(d.data.nodegroup[i]) < 0) {
                match2 =0;
              } 
            } 
          }
          return match2 || match1;
        });

        if (d.group == 1) {
          d3.select("#info1").html("<center><h2>Toto je množina " + d.id + " s velikostí " + d.value2 + "<h1><center>"); 
        }else {
          var val =d.id[0];
          for(count = 1; count < d.group; count++){
            val += ','+d.id[count] 
          }
          d3.select("#info1").html("<center><h2>Toto je sjednocení množin " + val + " s velikostí " + d.value2 + "<h1><center>"); 
        }

    }

      function handleMouseOut(d, i) {  // Add interactivity


        // d3.select(this).append('text');
        d3.selectAll(".highlight")
        .style("opacity", 0);
        d3.select("#info1").html("");

      }


      graph = transactionsdata
        var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
        .attr("stroke-width", function(d) { return Math.sqrt(d.value); })
        .attr("fill", function(d) { return color(0); });

        var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("nodes")
        .data(graph.nodes)
        .enter().append("g")
    // .on("mouseover", handleMouseOver)
    // .on("mouseout", handleMouseOut);
    // .attr("class", "supernodes");

    function nodeTransform(d) {
      d.x =  Math.max(maxNodeSize, Math.min(width - (d.value/2 || 16), d.x));
      d.y =  Math.max(maxNodeSize, Math.min(height - (d.value/2 || 16), d.y));
      return "translate(" + d.x + "," + d.y + ")";
    }

    node.append("title")
    .text(function(d) { return d.id; });


    // arcs

    var path = d3.arc()
    .outerRadius(function (d) {
      return (Math.pow(d.data.size,1/4)*6+6);
    })
    .innerRadius(0);

    var arc = node.selectAll(".arc")
    .data(function(d){
      var foo = new Array();
      for(count = 0; count < d.group; count++){
        var val ={"label":d.id[count], "value":1 , "size":d.value2, "nodegroup":d.id};
        foo.push(val);
      }
      return pie(foo);})
    .enter().append("g")
    .attr("class", "arc");


    var arcBorder = d3.arc()
    .outerRadius(function (d) {
      return (Math.pow(d.data.size,1/4)*6+8);
    })
    .innerRadius(function (d) {
      return (Math.pow(d.data.size,1/4)*6+6);
    });

    arc.append("path")
    .attr("fill", "black")
    .attr("d", arcBorder);

    arc.append("path")
    .attr("d",path)
    .attr("fill", function(d) {  return color(d.data.label); });
    // .on("mouseover", handleMouseOver)



// texty
node.append("text")
.attr("text-anchor", "middle")  
.text(function (d) {
  if (d.group > 1) {
    return d.id;
  }else{
    return "";
  }
} );

node.append("text")
.attr("text-anchor", "middle")  
.style("transform", "translate(0px,-15px)")
.text(function (d) {
  return d.text
} );

// pridani grafu



// eventy a simulace

// var setEvents = node
// .on( 'click', function (d) {
//   if (d.group == 1) {
//     d3.select("#info2").html("Toto je mnozina " + d.id + " s velikosti " + d.value); 
//   }else {
//     var val =d.id[0];
//     for(count = 1; count < d.group; count++){
//       val += ','+d.id[count] 
//     }
//     d3.select("#info2").html("Toto je sjednoceni mnozin " + val + " s velikosti " + d.value); 
//   }
//   console.log(d);
// })


var over= node
.on("mouseover", handleMouseOver)
.on("mouseout", handleMouseOut);

simulation
.nodes(graph.nodes)
.on("tick", ticked);

simulation.force("link")
.links(graph.links);



function ticked() {
  link
  .attr("x1", function(d) { return d.source.x; })
  .attr("y1", function(d) { return d.source.y; })
  .attr("x2", function(d) { return d.target.x; })
  .attr("y2", function(d) { return d.target.y; });

  node
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  node.attr("transform", nodeTransform);  
            // .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
          }

    }
    console.log("beff3")
    f2();