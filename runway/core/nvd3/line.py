import json

_javascript = """
$(function() {{
  nv.addGraph(function() {{
    var chart = nv.models.lineChart()
      .margin({{left: 100}})  //Adjust chart margins to give the x-axis some breathing room.
      .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
      .transitionDuration(350)  //how fast do you want the lines to transition?
      .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
      .showYAxis(true)        //Show the y-axis
      .showXAxis(true)        //Show the x-axis
      .x(function(d,i) {{ return i }})
      .y(function(d,i) {{return d[1] }})
    ;
    
    data = {data};
    
    chart.xAxis     //Chart x-axis settings
        .axisLabel('{x_label}')
      ;
    
    chart.xAxis.tickFormat(function(d) {{
      var dx = data[0].values[d] && data[0].values[d][0] || '';
      //var dx = data[0].values[d][0];
      //console.log(data[0].values[d][0]);
      //console.log(dx);
      //return d3.time.format('%d/%m/%y')(new Date(dx))
      return dx;
      return d3.time.format('%d/%m/%y')(new Date(dx))
    }});
      
    chart.yAxis     //Chart y-axis settings
        .axisLabel('{y_label}')
        //.tickFormat(d3.format('f'));
        .tickFormat(d3.format('{tick_format}'));
    
    // chart.forceY([50,100]);
    
    d3.select('#{div} svg')    //Select the <svg> element you want to render the chart in.   
        .datum(data)         //Populate the <svg> element with chart data...
        .call(chart);          //Finally, render the chart!

    // Update the chart when window resizes.
    nv.utils.windowResize(function() {{ chart.update() }});
    return chart;
  }});
}});
"""

# http://nvd3.org/examples/linePlusBar.html
def line_chart(start_date, end_date, lines, x_label="Month", y_label="Overall score (%)", tick_format="f"):
    """
    Example tick formats
    
    f -- Standard number
    ,.3f -- Float with 3 decimal points
    """
  
  
    # Example data
    # [
    #   {
    #     // Note, you can use 2 length lists instead of dicts
    #     values: [{x: 1, y: 13}, {x: 2, y: 16}, {x: 3, y: 21}],
    #     key: 'Line 1',
    #     color: '#AA0000'
    #   },
    #   {
    #     values: [{x: 1, y: 13}, {x: 2, y: 16}, {x: 3, y: 21}],
    #     key: 'Line 2',
    #     color: '#FF6600'
    #   }
    # ]
    
    data = list(lines)
    return lambda div: _javascript.format(div=div, data=data, x_label=x_label, y_label=y_label, tick_format=tick_format)
