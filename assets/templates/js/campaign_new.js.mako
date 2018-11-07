<%def name="insert()">
<script type="text/javascript">

function go_home() {
    window.location.href = '${attributes['home_path']}';
}

function submit_form() {
    document.getElementById("campaign_form").submit();
}

</script>
</%def>
