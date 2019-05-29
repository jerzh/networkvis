radius = 50;
rlarge = 5 * radius;

// wow I basically ended up learning an entire new framework for this project
// (D3) but it was worth it
// AJAX call to get data from server, then process data
d3.json('network_json', {}).then(function(data) {
  // if empty, don't do anything (so we don't get null errors)
  if (Object.entries(data).length === 0 && data.constructor === Object) {
    return;
  }

  var nodes_data = data['nodes_data'];
  var nodes_all = data['nodes_all'];
  var links_data = data['links_data'];

  // set svg size based on radius and number of nodes
  width = height = 6 * radius * (nodes_data.length ** 0.5) + 2 * rlarge;

  // create svg element
  var svg = d3.select('#graph')
    .append('svg')
      // .attr('xmlns', 'http://www.w3.org/2000/svg')
      .attr('width', width)
      .attr('height', height);

  // foreignObject test - don't forget to capitalize the o in foreignObject...
  // var inside = svg.append('foreignObject')
  //     .attr('x', 100)
  //     .attr('y', 100)
  //     .attr('width', 100)
  //     .attr('height', 100)
  //   .append('xhtml:p')
  //     .attr('xmlns', 'http://www.w3.org/1999/xhtml')
  //     .text('hello');

  // define simulation with some forces
  var simulation = d3.forceSimulation()
    .nodes(nodes_data)
    .force('charge_force', d3.forceManyBody().strength(-2 * (radius ** 2)))
    .force('x_force', d3.forceX(width / 2, 0.1))
    .force('y_force', d3.forceY(height / 2, 0.1))
    .force('collide_force', d3.forceCollide(radius));

  // determine innerHTML of node
  function innerHTML(d) {
    if (d.innerHTML != null) {
      return d.innerHTML;
    } else if (nodes_all['innerHTML'] != null) {
      return nodes_all['innerHTML'];
    } else {
      return '';
    }
  }

  // define a force for each link
  var link_force = d3.forceLink(links_data)
    .id(function(d) {
      if (d.id != null) {
        return d.id;
      } else {
        return d.name;
      }
    })
    .distance(3 * radius);

  // add to simulation
  simulation.force('links', link_force)

  // draw links
  var link = svg.append('g')
      .classed('links', true)
    .selectAll('line')
    .data(links_data)
    .enter()
    .append('line')
      .attr('stroke-width', 2)
      .style('stroke', function(d) { return d.color; });

  // draw nodes (so nodes go on top)
  var node = svg.append('g')
      .classed('nodes', true)
    .selectAll('circle')
    .data(nodes_data)
    .enter()
    .append('g');

  node.append('circle')
    .attr('r', radius)
    .attr('fill', function(d) { return d.color; });

  // click + drag functionality (adding it here so I can enable/disable it for
  // base state/expand state)
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
    .on('start', drag_start)
    .on('drag', drag_drag)
    .on('end', drag_end);

  // each node has two states: base and expanded
  // function to set base state: puts text elements
  function base(n) {
    // title text
    n.append('text')
      .classed('hover-underline', true)
      .attr('text-anchor', 'middle')
      .attr('alignment-baseline', 'central')
      .text(function(d) { return d.name; })
      .on('click', show);

    // add button
    n.filter(function(d) {
        return d.addable == 'true' || (d.addable == null && nodes_all['addable'] == 'true');
      })
      .append('text')
      .classed('hover-show', true)
      .attr('text-anchor', 'middle')
      .attr('transform', 'translate(' + 0 + ',' + (radius - 10) + ')')
      .attr('font-size', 'large')
      .html('&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;')
      .on('click', add);

    // delete button
    n.filter(function(d) {
        return d.deletable == 'true' || (d.deletable == null && nodes_all['deletable'] == 'true');
      })
      .append('text')
      .classed('hover-show', true)
      .attr('text-anchor', 'middle')
      .attr('transform', 'translate(' + 0 + ',-' + (radius - 20) + ')')
      .attr('font-size', 'large')
      .html('&nbsp;&nbsp;&nbsp; – &nbsp;&nbsp;&nbsp;')
      .on('click', del);

    // color text black or white according to how dark the circle is (found online)
    n.selectAll('text')
      .style('fill', function(d) {
        var c = getComputedStyle(d3.select(this.parentNode).select('circle').node()).fill.match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
        return (c[1] * 0.299 + c[2] * 0.587 + c[3] * 0.114) > 186 ? 'black' : 'white';
      });

    // black border if circle is white
    n.select('circle')
      .filter(function(d) {
        var c = getComputedStyle(d3.select(this.parentNode).select('circle').node()).fill.match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$/i);
        return c[1] == 0 && c[2] == 0 && c[3] == 0;
      })
      .style('stroke', 'white');

    // turn on dragging functionality
    drag_handler(n);
  }

  // set base state (at start)
  base(node);

  // function to set expand state: put foreignObject
  function expand(d, n, actualHTML) {
    var container = n.parentNode;

    // fix node
    d.fx = d.x;
    d.fy = d.y;

    // expand circle
    d3.select(container)
      .select('circle')
      .transition()
      .attr('r', rlarge + radius);

    // create and expand foreignObject
    fObj = d3.select(container)
      .append('foreignObject');

    fObj.transition()
      .attr('transform', 'translate(-' + rlarge + ',-' + rlarge + ')')
      .attr('width', 2 * rlarge)
      .attr('height', 2 * rlarge);

    // put some divs in foreignObject
    content = fObj.append('xhtml:div')
      .classed('content', true)
      .html(actualHTML);

    // when user leaves expanded node, contract
    content.on('mouseleave', function(d) {
      var container = this.parentNode;

      // no longer fixed
      d.fx = null;
      d.fy = null;

      // contract circle
      d3.select(container.parentNode)
        .select('circle')
        .transition()
        .attr('r', radius);

      // contract foreignObject
      d3.select(container)
        .transition()
        .attr('transform', 'translate(-' + 0 + ',-' + 0 + ')')
        .attr('width', 0)
        .attr('height', 0)
        .on('end', function(d) {
          // set base state again (after contraction)
          base(d3.select(this.parentNode))
          // remove foreignObject
          this.remove();
        })

      // reset collide_force and restart simulation
      simulation.force('collide_force', d3.forceCollide(radius))
        .on('tick', tickActions)
        // .alpha(1)
        .restart();
    })

    // remove text elements
    d3.select(container)
      .selectAll('text')
      .remove();

    // change collide_force to adjust for new node size and restart simulation
    simulation.force('collide_force', d3.forceCollide().radius(function(d0) {
        if (d0 == d) {
          return rlarge + radius;
        } else {
          return radius;
        }
      }))
      .on('tick', tickActions)
      // this line jostles the nodes slightly
      .alpha(1)
      .restart();

    // turn off dragging functionality (thank me later)
    d3.select(container).on('mousedown.drag', null);
  }

  // actualHTML is innerHTML
  function show(d) {
    expand(d, this, innerHTML);
  }

  // actualHTML is addPageForm
  function add(d) {
    addPageForm = addPageForm.replace('<br></textarea>', '</textarea>');
    var form = "<form action='" + formAction + "' method='post' autocomplete='off'>"
      + addPageForm
      + "<input type='submit' name='add_page_form' value='Add'>"
      + "<input type='hidden' name='id' value='" + d.id + "'>"
      + "</form>";
    expand(d, this, form);
  }

  // actualHTML is delPageForm
  function del(d) {
    var form = "<form action='" + formAction + "' method='post' autocomplete='off'>"
      + delPageForm
      + "<input id='del-submit' type='submit' name='del_page_form' value='Delete' disabled='disabled'>"
      + "<input type='hidden' name='id' value='" + d.id + "'>"
      + "</form>";
    expand(d, this, '<h1 style="text-align: center"> Are you sure you want to delete this page? Type its title below to confirm: </h1>' + form);
    d3.select('#id_field').on('keyup', function() {
      if (this.value == d.name) {
        d3.select('#del-submit')
          .attr('disabled', null);
      } else {
        d3.select('#del-submit')
          .attr('disabled', 'disabled');
      }
    });
  }

  // function to update the locations of the nodes and links after every tick
  function tickActions() {
    node.attr('transform', function(d) { return 'translate(' + d.x + ',' + d.y + ')'; });

    // bounding box (decided against it since nodes gravitate to center anyway)
    // node.attr('transform', function(d) { return 'translate('
    //   + (d.x = Math.max(radius, Math.min(width - radius, d.x))) + ','
    //   + (d.y = Math.max(radius, Math.min(height - radius, d.y))) + ')'; });

    link.attr('x1', function(d) { return d.source.x; })
     .attr('y1', function(d) { return d.source.y; })
     .attr('x2', function(d) { return d.target.x; })
     .attr('y2', function(d) { return d.target.y; });
  }

  // add above function to simulation
  simulation.on('tick', tickActions);
});
