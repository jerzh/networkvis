radius = 50;
rlarge = 5 * radius;

// get browser size
// var w = window,
//   d = document,
//   e = d.documentElement,
//   g = d.getElementsByTagName('body')[0],
//   width = w.innerWidth || e.clientWidth || g.clientWidth,
//   height = w.innerHeight|| e.clientHeight|| g.clientHeight;

// get browser size (with jQuery!)
// width = $(document).width();
// height = $(document).height();

var nodes_data =  [
    {"name": "Lillian", "sex": "F"},
    {"name": "Gordon", "sex": "M"},
    {"name": "Sylvester", "sex": "M"},
    {"name": "Mary", "sex": "F"},
    {"name": "Helen", "sex": "F"},
    {"name": "Jamie", "sex": "M"},
    {"name": "Jessie", "sex": "F"},
    {"name": "Ashton", "sex": "M"},
    {"name": "Duncan", "sex": "M"},
    {"name": "Evette", "sex": "F"},
    {"name": "Mauer", "sex": "M"},
    {"name": "Fray", "sex": "F"},
    {"name": "Duke", "sex": "M"},
    {"name": "Baron", "sex": "M"},
    {"name": "Infante", "sex": "M"},
    {"name": "Percy", "sex": "M"},
    {"name": "Cynthia", "sex": "F"}
]

// set svg size based on radius and number of nodes
width = height = 2 * nodes_data.length * radius;

var links_data = [
    {"source": "Sylvester", "target": "Gordon", "type":"A"},
    {"source": "Sylvester", "target": "Lillian", "type":"A"},
    {"source": "Sylvester", "target": "Mary", "type":"A"},
    {"source": "Sylvester", "target": "Jamie", "type":"A"},
    {"source": "Sylvester", "target": "Jessie", "type":"A"},
    {"source": "Sylvester", "target": "Helen", "type":"A"},
    {"source": "Helen", "target": "Gordon", "type":"A"},
    {"source": "Mary", "target": "Lillian", "type":"A"},
    {"source": "Ashton", "target": "Mary", "type":"A"},
    {"source": "Duncan", "target": "Jamie", "type":"A"},
    {"source": "Gordon", "target": "Jessie", "type":"A"},
    {"source": "Sylvester", "target": "Fray", "type":"E"},
    {"source": "Fray", "target": "Mauer", "type":"A"},
    {"source": "Fray", "target": "Cynthia", "type":"A"},
    {"source": "Fray", "target": "Percy", "type":"A"},
    {"source": "Percy", "target": "Cynthia", "type":"A"},
    {"source": "Infante", "target": "Duke", "type":"A"},
    {"source": "Duke", "target": "Gordon", "type":"A"},
    {"source": "Duke", "target": "Sylvester", "type":"A"},
    {"source": "Baron", "target": "Duke", "type":"A"},
    {"source": "Baron", "target": "Sylvester", "type":"E"},
    {"source": "Evette", "target": "Sylvester", "type":"E"},
    {"source": "Cynthia", "target": "Sylvester", "type":"E"},
    {"source": "Cynthia", "target": "Jamie", "type":"E"},
    {"source": "Mauer", "target": "Jessie", "type":"E"}
]

// create svg element
var svg = d3.select("#graph")
  .append("svg")
    // .attr("xmlns", "http://www.w3.org/2000/svg")
    .attr("width", width)
    .attr("height", height);

// foreignObject test - don't forget to capitalize the o in foreignObject...
// var inside = svg.append("foreignObject")
//     .attr("x", 100)
//     .attr("y", 100)
//     .attr("width", 100)
//     .attr("height", 100)
//   .append("xhtml:p")
//     .attr("xmlns", "http://www.w3.org/1999/xhtml")
//     .text("hello");

// define simulation with some forces
var simulation = d3.forceSimulation()
  .nodes(nodes_data)
  .force("charge_force", d3.forceManyBody().strength(-2 * (radius ** 2)))
  .force("x_force", d3.forceX(width / 2, 0.1))
  .force("y_force", d3.forceY(height / 2, 0.1))
  .force("collide_force", d3.forceCollide(radius));

// function to choose color
function circleColor(d){
    if(d.sex =="M"){
        return "blue";
    } else {
        return "pink";
    }
}

// define a force for each link
var link_force = d3.forceLink(links_data)
  .id(function(d) { return d.name; })
  .distance(3 * radius);

// add to simulation
simulation.force("links", link_force)

// function to choose color
function linkColor(d){
    console.log(d);
    if(d.type == "A"){
        return "green";
    } else {
        return "red";
    }
}

// draw links
var link = svg.append("g")
    .attr("class", "links")
  .selectAll("line")
  .data(links_data)
  .enter()
  .append("line")
    .attr("stroke-width", 2)
    .style("stroke", linkColor);

// draw nodes (so nodes go on top)
var node = svg.append("g")
    .attr("class", "nodes")
  .selectAll("circle")
  .data(nodes_data)
  .enter()
  .append("g");

node.append("circle")
  .attr("r", radius)
  .attr("fill", circleColor);

var text = node.append("text")
  .attr("text-anchor", "middle")
  .attr("alignment-baseline", "central")
  .text("hello")
  .on("mouseenter", handleMouseEnter);

function handleMouseEnter(d) {
  var container = this.parentNode;

  d.fx = d.x;
  d.fy = d.y;

  d3.select(container)
    .select("circle")
    .transition()
    .attr("r", rlarge + radius);

  fObj = d3.select(container)
    .append("foreignObject");

  fObj.transition()
    .attr("transform", "translate(-" + rlarge + ",-" + rlarge + ")")
    .attr("width", 2 * rlarge)
    .attr("height", 2 * rlarge);

  content = fObj.append("xhtml:div")
    .classed("content", true);

  content.append("div")
      .classed("content-2", true)
    .append("p")
      .text("wow much change");

  content.on("mouseleave", function(d) {
    var container = this.parentNode;

    d.fx = null;
    d.fy = null;

    d3.select(container.parentNode)
      .select("circle")
      .transition()
      .attr("r", radius);

    d3.select(container)
      .transition()
      .attr("transform", "translate(-" + 0 + ",-" + 0 + ")")
      .attr("width", 0)
      .attr("height", 0)
      .on("end", function(d) {
        d3.select(this.parentNode).append("text")
          .attr("text-anchor", "middle")
          .attr("alignment-baseline", "central")
          .text("hello")
          .on("mouseenter", handleMouseEnter);
        this.remove();
      })

    simulation.force("collide_force", d3.forceCollide(radius))
      .on("tick", tickActions)
      // .alpha(1)
      .restart();
  })

  d3.select(this)
    .remove();

  simulation.force("collide_force", d3.forceCollide().radius(function(d0) {
    if (d0 == d) {
      return rlarge + radius;
    } else {
      return radius;
    }
  }))
    .on("tick", tickActions)
    .alpha(1)
    .restart();
}

// function to update the locations of the circles after every tick
function tickActions() {
  // wrong radius; will hopefully fix later
  node.attr("transform", function(d) { return "translate("
  + Math.max(radius, Math.min(width - radius, d.x)) + ","
  + Math.max(radius, Math.min(height - radius, d.y)) + ")"; });

  link.attr("x1", function(d) { return d.source.x; })
   .attr("y1", function(d) { return d.source.y; })
   .attr("x2", function(d) { return d.target.x; })
   .attr("y2", function(d) { return d.target.y; });
}

// add to simulation
simulation.on("tick", tickActions)

// click + drag functionality
function drag_start(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function drag_drag(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function drag_end(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

var drag_handler = d3.drag()
  .on("start", drag_start)
  .on("drag", drag_drag)
  .on("end", drag_end);

drag_handler(node)

// resize when window resized
// function updateWindow(){
//     svg.attr("width", $(document).width()).attr("height", $(document).height());
// }
// d3.select(window).on('resize.updatesvg', updateWindow);
