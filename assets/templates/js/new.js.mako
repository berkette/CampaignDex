<%namespace name="js_common" file="${context['attributes']['js_common']}"/>

<%def name="insert()">
<script>

${js_common.insert()}

function submit_form() {
    document.getElementById("new_page_form").submit()
}

</script>
</%def>
