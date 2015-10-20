from ....core.widgets.models import JSWidget

class UserPicker(JSWidget):
    """
    Instructions:
    
    data-toggle="modal" data-target="#myModal"
    
    """
    
    js_libs  = ()
    css_libs = ()
    
    initial_raw_js = (
"""
$(function () {
  $('[data-toggle="popover"]').popover();
});
""",
"""
var user_picker_target = "";

function user_picker (new_target) {
    user_picker_target = $(new_target);
    
    $('#user_picker_username').val('');
    $('#user_picker_modal_results').html('');
    $('#user_picker_modal').modal({});
    
    window.setTimeout(function () {$('#user_picker_username').focus();}, 1);
}

function user_picker_select (selection) {
    $('#user_picker_username').val('');
    $('#user_picker_modal_results').html('');
    
    user_picker_target.val(selection);
    $('#user_picker_modal').modal('hide');
    
    window.setTimeout(function () {user_picker_target.focus();}, 1);
}

function user_picker_display (results) {
    if (results == "") {return;}
    
    $('#user_picker_modal_results').html('');
    
    var new_html = "";
    var username = "";
    var display_name = "";
    
    split_results = results.split('\\n');
    for (var i = 0; i < split_results.length; i++) {
        username = split_results[i].split("|")[0];
        display_name = split_results[i].split("|")[1];
        
        new_html += '<div class="user_picker_row" onclick="user_picker_select(\\'' + username + '\\');">' + display_name + ' (' + username + ')</div>';
    }
    
    $('#user_picker_modal_results').html(new_html);
}
""",
# """
# // For fasting testing, comment out when not being manually tested
# $(function () {
#   user_picker('#username_search');
#   $('#user_picker_username').val('r');
#   user_picker_search();
# });
# """
)

    extra_raw_js = """
function user_picker_search () {{
    search_value = $('#user_picker_username').val();
    
    if (search_value.length < 3) {{return;}}
    
    $.ajax({{
        url: "{ajax_url}",
        data: {{"username":search_value}}
    }}).done(
        user_picker_display
    );
}}
"""
    raw_css = """
.user_picker_row {
    padding: 3px 5px;
    cursor: pointer;
}

.user_picker_row:hover {
    background-color: #DDF;
}
    
"""
    
    raw_html = """
<div class="modal fade" id="user_picker_modal" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">User search</h4>
      </div>
      
      <div class="modal-body">
        <form action="#" method="post" class="form-horizontal" onsubmit="user_picker_search(); return false;">
          <div class="form-group">
            <div class="col-sm-10">
              <input type="text" name="username" id="user_picker_username" value="" placeholder="" class="form-control" />
            </div>
            <div class="col-sm-2">
              <!-- <input type="submit" value="Submit" name="form.submitted" class="btn btn-primary pull-right" />
              -->
              
              <div class="btn btn-primary" onclick="user_picker_search();">
                &nbsp;<i class="fa fa-search fa-fw"></i>&nbsp;
              </div>
            </div>
          </div>
          
        </form>
        
        <div id="user_picker_modal_results">
        
        </div>

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
            ajax_url = request.route_url('ajax.user.search'),
        ),)
        
        super(UserPicker, self).__init__(request)

