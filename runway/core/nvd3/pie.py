import json

_javascript = """
$(function() {{
    var data = {data};

    // PIE CHART
    nv.addGraph(function() {{
        var chart = nv.models.pieChart()
            .x(function(d) {{ return d.label }})
            .y(function(d) {{ return d.value }})
            .showLabels(true);
          
          chart.color({colours});
          
          d3.select('#{div} svg')
              .datum(data)
              .transition().duration(350)
              .call(chart);
    
    return chart;
    }});
}});
"""

def pie_chart(data):
    # Example data
    # [
    #     {'label':'Red', 'value': 1, 'colour':'#AA0000'},
    #     {'label':'Amber', 'value': 23, 'colour':'#FF6600'},
    #     {'label':'Green', 'value': 76, 'colour':'#00AA00'},
    # ]
    
    # Colours
    colours = [d['colour'] for d in data]
    
    return lambda div: _javascript.format(div=div, data=data, colours=colours)