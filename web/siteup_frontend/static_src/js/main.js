$(function () {
    var render, renderGraphs;

    render = function (data, canvas) {
        var add_gradient, area, bad_at, dateEnd, dateStart, daySpan, format, gradient, h, line, lines, main_path, max, min, numdays, padb, padl, padr, padt, subs, ticks, timeFormat, transition, units, vis, w, warn_at, x, xAxis, y, yAxis, yax, _ref;
        w = canvas.width();
        h = canvas.height();

        console.log(w,h);

        units = canvas.attr('data-unit');
        add_gradient = canvas.attr('data-warn-at') != null;
        if (!data.length) {
            return;
        }
        format = function (d) {
            return d + units;
        };
        timeFormat = function (d) {
            if (d < 60) {
                return "" + d + "m";
            } else {
                return "" + (d / 60) + "h";
            }
        };
        data = data.map(function (d, i) {
            return [new Date(d[0] * 1000), d[1]];
        }).sort(function (a, b) {
            return d3.ascending(a[0], b[0]);
        });
        numdays = data.length;
        _ref = [6, 50, 2, 16], padt = _ref[0], padl = _ref[1], padr = _ref[2], padb = _ref[3];
        max = d3.max(data, function (d) {
            return d[1];
        });
        min = d3.min(data, function (d) {
            return d[1];
        });
        if (units === '%') {
            if (max === min) {
                max = 100;
            }
            if (!(min < 99)) {
                min = 99;
            }
        }
        dateStart = data[0][0];
        dateEnd = data[data.length - 1][0];
        daySpan = Math.round((dateEnd - dateStart) / (1000 * 60 * 60 * 24));
        x = d3.time.scale().domain([dateStart, dateEnd]).range([0, w - padl - padr]);
        y = d3.scale.linear().domain([min, max]).range([h - padb - padt, 0]);
        if (daySpan === 1) {
            ticks = 3;
            subs = 6;
        } else if (daySpan === 7) {
            ticks = 4;
            subs = 1;
        } else {
            ticks = 4;
            subs = 6;
        }
        xAxis = d3.svg.axis().scale(x).tickSize(5).tickSubdivide(subs).ticks(ticks).orient("bottom").tickFormat(function (d) {
            if (daySpan <= 1) {
                return d3.time.format('%H:%M')(d).replace(/\s/, '').replace(/^0/, '');
            } else {
                return d3.time.format('%m/%d')(d).replace(/\s/, '').replace(/^0/, '').replace(/\/0/, '/');
            }
        });
        yAxis = d3.svg.axis().scale(y).orient("left").tickPadding(5).tickSize(w).ticks(2).tickFormat(format);
        vis = d3.select(canvas.get(0)).data(data).append('svg').attr('width', w).attr('height', h + padt + padb).attr('class', 'viz').append('svg:g').attr('transform', "translate(" + padl + "," + padt + ")");
        if (add_gradient) {
            warn_at = parseFloat(canvas.attr('data-warn-at'));
            bad_at = parseFloat(canvas.attr('data-bad-at'));
            transition = warn_at - (warn_at - bad_at) / 2;
            gradient = vis.append("svg:defs").append("svg:linearGradient").attr("id", "gradient").attr("x1", "0%").attr("y1", "0%").attr("x2", "0%").attr("y2", "100%").attr("spreadMethod", "pad");
            gradient.append("svg:stop").attr("offset", 100 * y(warn_at) / h + '%').attr("stop-color", "#396").attr("stop-opacity", 1);
            gradient.append("svg:stop").attr("offset", 100 * y(transition) / h + '%').attr("stop-color", "#F29D50").attr("stop-opacity", 1);
            gradient.append("svg:stop").attr("offset", 100 * y(bad_at) / h + '%').attr("stop-color", "#c00").attr("stop-opacity", 1);
        }
        vis.append("g").attr("class", "x axis").attr('transform', "translate(0, " + (h - padt - padb) + ")").call(xAxis);
        area = d3.svg.area().x(function (d) {
            return x(d[0]);
        }).y0(function (d) {
            return y(d[1]);
        }).y1(function (d) {
            return y(0);
        }).interpolate('basis');
        line = d3.svg.line().x(function (d) {
            return x(d[0]);
        }).y(function (d) {
            return y(d[1]);
        }).interpolate('basis');
        yax = vis.append("g").attr("transform", "translate(" + w + ", 0)").attr("class", "y axis");
        yax.call(yAxis).selectAll('.y.axis g').classed('zero', function (d, i) {
            return d === 0;
        }).classed('add', function (d, i) {
            return d > 0;
        }).classed('del', function (d, i) {
            return d < 0;
        });
        lines = vis.selectAll('path.cumulative').data([data]).enter();
        main_path = lines.append('path').attr('class', 'path').attr('d', line);
        if (add_gradient) {
            if (d3.min(data, function (d) {
                return d[1];
            }) === 100) {
                return main_path.style("stroke", "#396");
            } else {
                return main_path.style("stroke", "url(#gradient)");
            }
        }
    };

    renderGraphs = function () {
        return $('.graph-container').html('').each(function () {
            console.log("WUT");
            var $canvas, data;
            $canvas = $(this);
            data = JSON.parse($canvas.attr('data-string') || '[]');
            return render(data, $canvas);
        });
    };

    renderGraphs();

});