<%def name="insert()">
function exit_campaign() {
    window.location.href = "${attributes['exit_path']}";
}

function go_to_home() {
    window.location.href = "${attributes['home_path']}";
}

function go_to_new() {
    var new_path = "${attributes['new_path']}";
% if 'page_path' in attributes:
    new_path = new_path + '?path=' + "${attributes['page_path']}";
% endif
    window.location.href = new_path;
}
</%def>
