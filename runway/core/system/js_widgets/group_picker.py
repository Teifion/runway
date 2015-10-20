from ....core.widgets.models import JSWidget

class GroupPicker(JSWidget):
    """
    Instructions:
    
    data-toggle="modal" data-target="#group_picker_modal"
    
    """
    
    js_libs  = ()
    css_libs = ()
    
    initial_raw_js = (
"""
$(function () {
  $('[data-toggle="popover"]').popover();
});

$(function () {
    $('#group_picker_modal').on('shown.bs.modal', function () {
      $('#group_picker_username').focus();
    })
});
""",
"""
var group_picker_target = "";
var group_picker_mode = 1;

function group_picker (new_target) {
    group_picker_mode = 1;
    launch_group_picker(new_target);
}

function group_multi_picker (new_target) {
    group_picker_mode = 2;
    launch_group_picker(new_target);
}

function launch_group_picker (new_target) {
    group_picker_target = $(new_target);
    
    $('#group_picker_username').val('');
    $('#group_picker_modal_results').html('');
    $('#group_picker_current').html('');
    $('#group_picker_modal').modal({});
    
    window.setTimeout(function () {$('#group_picker_username').focus();}, 200);
}

function group_picker_select (selection) {
    // $('#group_picker_username').val('');
    // $('#group_picker_modal_results').html('');
    
    if (group_picker_mode == 2) {
        if (group_picker_target.val() == "") {
          group_picker_target.val(selection);
        } else {
          group_picker_target.val(group_picker_target.val() + ", " + selection);
        }
    } else {
        group_picker_target.val(selection);
        $('#group_picker_modal').modal('hide');
        window.setTimeout(function () {group_picker_target.focus();}, 1);
    }
    
    $('#group_picker_current').html(group_picker_target.val());
    
    //$('#group_picker_modal').modal('hide');
    // window.setTimeout(function () {group_picker_target.focus();}, 1);
}

function group_picker_display (results) {
    if (results == "") {return;}
    
    $('#group_picker_modal_results').html('');
    
    var new_html = "";
    var username = "";
    var display_name = "";
    
    split_results = results.split('\\n');
    for (var i = 0; i < split_results.length; i++) {
        username = split_results[i].split("|")[0];
        display_name = split_results[i].split("|")[1];
        
        new_html += '<div class="group_picker_row" onclick="group_picker_select(\\'' + username + '\\');">' + display_name + ' (' + username + ')</div>';
    }
    
    $('#group_picker_modal_results').html(new_html);
}
""",
# """
# // For fasting testing, comment out when not being manually tested
# $(function () {
#   group_picker('#auditor');
#   $('#group_picker_username').val('ro');
#   group_picker_search();
# });
# """
)

    extra_raw_js = """
function group_picker_search () {{
    search_value = $('#group_picker_username').val();
    
    if (search_value.length < 3) {{return;}}
    
    $.ajax({{
        url: "{ajax_url}",
        data: {{"username":search_value}}
    }}).done(
        group_picker_display
    );
}}
"""
    raw_css = """
.group_picker_row {
    padding: 3px 5px;
    cursor: pointer;
}

.group_picker_row:hover {
    background-color: #DEF;
}
"""
    
    raw_html = """
<div class="modal fade" id="group_picker_modal" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Group search</h4>
      </div>
      
      <div class="modal-body">
        <form action="#" method="post" class="form-horizontal" onsubmit="group_picker_search(); return false;">
          <div class="form-group">
            <div class="col-sm-10">
              <input type="text" name="username" id="group_picker_username" value="" placeholder="" class="form-control" />
            </div>
            <div class="col-sm-2">
              <!-- <input type="submit" value="Submit" name="form.submitted" class="btn btn-primary pull-right" />
              -->
              
              <div class="btn btn-primary" onclick="group_picker_search();">
                &nbsp;<i class="fa fa-search fa-fw"></i>&nbsp;
              </div>
            </div>
          </div>
          
        </form>
        
        <div id="group_picker_modal_results">
        
        </div>
        
        <br />
        Currently: <span id="group_picker_current"></span>
      </div>
      
      <div class="modal-footer">
        <button type="button" class="btn btn-default btn-block" data-dismiss="modal">Close</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
"""

    def __init__(self, request):
        self.raw_js = self.initial_raw_js + (self.extra_raw_js.format(
            ajax_url = request.route_url('ajax.group.search'),
        ),)
        
        super(GroupPicker, self).__init__(request)

