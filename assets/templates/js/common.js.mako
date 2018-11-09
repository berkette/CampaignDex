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


<%def name="insert_quill()">
var quill;

function edit_page() {
    window.location.href = "${attributes['page_path']}?edit=true";
}

function initialize_quill(editor) {
    var container = document.getElementById('quill_editor')
    
    if (editor == true) {
        options = {
            modules: {
                toolbar: [
                    ['bold', 'italic'],
                    ['link', 'blockquote', 'code-block', 'image'],
                    [{ list: 'ordered' }, { list: 'bullet' }]
                ]
            },
            placeholder: 'Add some content...',
            theme: 'snow'
        };
    } else {
        options = {
            modules: {toolbar: []},
            readOnly: true,
            theme: 'snow'
        };
    }

    quill = new Quill(container, options);

    if (editor == false) {
        quill.enable(false);
    }
}

function save_page(apply) {
    var rtf = JSON.stringify(quill.getContents());
    $("#save_hidden").attr("value", rtf);

    if (apply = true) {
        $("#save_form").attr("action", "${attributes['apply_page']}");
    } else {
        $("#save_form").attr("action", "${attributes['save_page']}");
    }
    $("#save_form").submit();
}

function get_rtf_content() {
    $.getJSON("${attributes['rtf']}", function(data) { populate_page(data); });
}

function populate_page(data) {
    quill.setContents(data);
}

</%def>