import json

_javascript = """
$(function() {{
  nv.addGraph(function() {{
      var chart = nv.models.multiBarChart()
        .transitionDuration(350)
        .reduceXTicks(true)   //If 'false', every single x-axis tick label will be rendered.
        .rotateLabels(0)      //Angle to rotate x-axis labels.
        .showControls(true)   //Allow user to switch between 'Grouped' and 'Stacked' mode.
        .groupSpacing(0.1)    //Distance between each group of bars.
      ;
      
      data = {data};
      
      chart.xAxis
          //.tickFormat(function (d) {{return d3.time.format('%b %y')(new Date(2013, d))}});
          .tickFormat(function (d) {{return d}});
      
      chart.yAxis
          //.tickFormat(d3.format('d'));
          .tickFormat(d3.format(',.1f'));
      
      chart.stacked(true);
      
      d3.select('#{div} svg')
          .datum(data)
          .call(chart);

      nv.utils.windowResize(chart.update);
      return chart;
  }});
}});
"""

def column_chart(start_date, end_date, columns):
    # Example data
    # It runs based on the sets, not the columns
    # [
    #   {
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
    
    # Colours
    # colours = [d['colour'] for d in data]
    
    data = list(columns)
    return lambda div: _javascript.format(div=div, data=data)
