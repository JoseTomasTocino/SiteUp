function buildGraph(graphName, graphData) {
    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Date');
    if (graphData['type'] == "pingcheck") {
        data.addColumn('number', 'Resp. time');
    } else {
        data.addColumn('number', 'Status');
    }
    data.addRows(graphData['data']);

    var options = {
        backgroundColor: 'transparent',
        legend: 'none',
        /*chartArea: {
            left: 70,
            width: "78%" ,
        },//*/
        hAxis: {
            baselineColor: '#ddd',
            gridlines: { color: '#ddd' },
            minorGridlines: { color: '#ddd' },
        },
        vAxis: {
            gridlines: { color: '#ddd' },
            minorGridlines: { color: '#ddd' },
            baselineColor: '#ddd',
            format:'###ms',
        },
        series: {
            0: {
                color: '#46596a'
            }
        }
    };

    if (typeof graphData['is_single'] != "undefined") {
        options['chartArea'] = {
            width: "90%" ,
            top: 20,
            left: 70,
            height: "70%",
        };//*/
    }

    console.log(options['chartArea']);

    if (graphData['type'] == "pingcheck") {
        options['curveType'] = 'function';
    } else {
        options['vAxis']['viewWindow'] = {
            max: 1.25,
            min: -0.25
        }
        options['vAxis']['ticks'] = [{v:0, f:"Down"}, {v:1, f:"Up"}];
    }

    if (graphData['status'] != 0) {
        options['series'][0]['color'] = '#e83f40';
    }

    var container = document.querySelector(graphName);
    var chart = new google.visualization.LineChart(container);
    chart.draw(data, options);
}

if (typeof graphInfo != "undefined") {
    for (var graphName in graphInfo) {
        console.log("Plotting graph  " + graphName);
        buildGraph(graphName, graphInfo[graphName]);
    }
}