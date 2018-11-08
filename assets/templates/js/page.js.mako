<%namespace name="js_common" file="${context['attributes']['js_common']}"/>

<%def name="insert()">
<script>

${js_common.insert()}

function toggle_quicklink() {
    document.getElementById("quicklink_form").submit()
}

function go_to_superpage() {
    window.location.href = "${attributes['superpage_path']}";
}

</script>
</%def>
