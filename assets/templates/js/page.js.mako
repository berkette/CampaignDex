<%namespace name="js_common" file="${context['attributes']['js_common']}"/>

<%def name="insert()">
<script>

${js_common.insert()}
${js_common.insert_quill()}

function delete_page() {
    $("#delete_form").submit();
}

function toggle_quicklink() {
    $("#quicklink_form").submit();
}

function go_to_superpage() {
    window.location.href = "${attributes['superpage_path']}";
}

</script>
</%def>
