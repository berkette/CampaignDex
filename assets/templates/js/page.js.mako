<%namespace name="js_common" file="${context['attributes']['js_common']}"/>

<%def name="insert()">
<script>

${js_common.insert()}

var quill;

function edit_page() {
    window.location.href = "${attributes['page_path']}?edit=true";
}

function save_page(apply) {
    var rtf = JSON.stringify(quill.getContents());
    document.getElementById("save_hidden").value = rtf;
    form = document.getElementById("save_form");

    if (apply = true) {
        form.action = "${attributes['apply_page']}";
    } else {
        form.action = "${attributes['save_page']}";
    }
    form.submit();
}

function populate_page() {
    if ("${attributes['rtf_content']}".length > 0) {
        var rtf = JSON.parse('${attributes['rtf_content']}');
        quill.setContents(rtf);
    }
}

function toggle_quicklink() {
    document.getElementById("quicklink_form").submit()
}

function go_to_superpage() {
    window.location.href = "${attributes['superpage_path']}";
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

</script>
</%def>
