function fetchGraphData(graphName, graphData) {

    // Fetch data via AJAX only if the data is not previously defined
    if (typeof graphData['data'] == "undefined") {
        graphData['data'] = [];

        var ajaxUrl = base_url + '/get_dashboard_graph_data/' + graphData['type'] + '/' + graphData['id'];

        $.getJSON(ajaxUrl, function(data) {
            graphData['data'] = data;

            buildGraphD3(graphName, graphData);
        });
    }

    // Detail page already has the data
    else {
        buildGraphD3(graphName, graphData);
    }
}

function buildGraphD3(graphName, graphData) {
    var x, y, xDomain, yDomain, xAxis, yAxis;
    var data = graphData['data'];

    var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = $(graphName).width() - margin.left - margin.right,
    height = $(graphName).height() - margin.top - margin.bottom;

    // Preprocess data
    data.forEach(function(d) {
        var dstr = d[0];

        // Remove miliseconds and the T divisor
        dstr = dstr.substr(0, dstr.lastIndexOf('.')).replace('T', ' ');

        // Build the date
        d[0] = new Date(dstr);
    });

    var format = d3.time.format.multi([
      [".%L", function(d) { return d.getMilliseconds(); }],
      [":%S", function(d) { return d.getSeconds(); }],
      ["%H:%M", function(d) { return d.getMinutes(); }],
      ["%H:00", function(d) { return d.getHours(); }],
      ["%a %d", function(d) { return d.getDay() && d.getDate() != 1; }],
      ["%b %d", function(d) { return d.getDate() != 1; }],
      ["%B", function(d) { return d.getMonth(); }],
      ["%Y", function() { return true; }]
    ]);

    // Init X scale3
    // d3.extent returns minimum and maximum

    x = d3.time.scale.utc()
        .range([0, width])
        .domain(d3.extent(data, function(d) { return d[0]; }));

    //x.ticks(2);

    xAxis = d3.svg.axis()
            .scale(x)
            .tickFormat(format)
            .ticks(8)
            .orient("bottom");

    // Init Y scale
    if (graphData['type'] == 'pingcheck') {
        yDomain = d3.extent(data, function(d) { return d[1]; });

        // When the graph only has one value, the domain min and max are the same
        // Artificially adding some "padding" keeps the graph cool

        if (yDomain[0] == yDomain[1]) {
            yDomain[0] -= 5;
            yDomain[1] += 50;
        }

    } else {
        yDomain = [-0.25, 1.25];
    }

    y = d3.scale.linear()
        .range([height, 0])
        .domain(yDomain);

    if (graphData['type'] == 'pingcheck') {
        // Init Y axis
        yAxis = d3.svg.axis()
            .scale(y)
            .ticks(5)
            .tickFormat(function(d) {
                return d + "ms";
            })
            .orient("left");
    } else {
        yAxis = d3.svg.axis()
            .scale(y)
            .ticks(2)
            .tickFormat(function(d) {
                if (d == 0) {
                    return "Down";
                } else {
                    return "Up";
                }
            })
            .orient("left");
    }

    // Init line
    var line = d3.svg.line()
        .x(function(d) { return x(d[0]); })
        .y(function(d) { return y(d[1]); });

    $(graphName).find('svg').remove();

    var baseSvg = d3.select(graphName).append("svg")
        .style('opacity', '0')
        .style('display', 'none')
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    var svg = baseSvg
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "grid")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_axis()
            .tickSize(-height, 0, 0)
            .tickFormat("")
        )

    function make_x_axis(scale) {
        return d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(10)
    }

    function make_y_axis() {
        return d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(5)
    }

    svg.append("g")
        .attr("class", "grid")
        .call(make_y_axis()
            .tickSize(-width, 0, 0)
            .tickFormat("")
        )

    // Build data
    svg.append("path")
        .datum(data)
        .attr("class", "line data-line")
        .attr("d", line);

    // Build first group, container
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Build second group, axes
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)

        /*
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Price ($)") //*/


    $(graphName).find('.placeholder').fadeOut(function(){
        baseSvg
            .style('display', 'block')
            .transition()
            .duration(400)
            .style('opacity', 1);
    });
}


function buildGraphs() {
    if (typeof graphInfo != "undefined") {
        for (var graphName in graphInfo) {
            fetchGraphData(graphName, graphInfo[graphName]);
        }
    }
}

// TABBED detail page

$(".tabs").each(function(){
    $(".tabs-header a").on('click', function(e){

        // Get the tab number
        var tabNumber = $(this).index();

        // Remove active class from current tab button
        $(this).siblings('a').removeClass('active');

        // Set current tab button to 'active'
        $(this).addClass('active');

        // Hide tab content
        var currentTab = $(this).closest('.tabs').find('.tabs-content')
            .hide()

            // Show only the content linked to the current tab
            .eq(tabNumber)
            .show()
        ;

        // Get graph's uniquename
        graphName = currentTab.find('.detail-graph').data('uniquename');

        // Draw graph
        fetchGraphData(graphName, graphInfo[graphName])

        e.preventDefault();
    });
});

// Enhanced help text for fields
$(".more-help a").on('click', function(e){
    e.preventDefault();
    $(this).parent().find('div').slideToggle();
});

$(window).load(function()
{
    if ($('body').hasClass('section-dashboard')) {
        buildGraphs();
    }
    // Force show first tab
    $(".tabs-header a").eq(0).click();
});

$('.drag-number-widget').each(function(i, e) {
    var theDealer = $(this)[0];
    var $target = $("#" + $(this).data('target'));
    var min = parseInt($(this).data('min'));
    var max = parseInt($(this).data('max'));
    var stepVal = parseInt($(this).data('steps'));
    var curVal = (parseInt($target.val()) - min)  / (max - min);

    var d = new Dragdealer(theDealer, {
        steps: stepVal,
        animationCallback: function(x, y) {
            var value = Math.round(min + x * (max - min));
            $(theDealer).find('.handle').text(value);
            $target.val(value);
        }
    });

    d.setValue(curVal, 0, true);
});