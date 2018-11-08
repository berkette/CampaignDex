<%def name="insert()">
function exit_campaign() {
    document.cookie = "${attributes['cookie_id']}" + '=;';
    document.cookie = "${attributes['cookie_db']}" + '=;';
    document.cookie = "${attributes['cookie_skin']}" + '=;';
    window.location.href = "${attributes['home_path']}?exit=true";
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
