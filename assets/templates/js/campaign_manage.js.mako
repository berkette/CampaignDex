<%def name="insert()">
<script type="text/javascript">

function delete_campaign() {
    confirmation = confirm("Are you sure? This will delete all campaign data.");
    if (confirmation == true) {
        document.getElementById("delete_form").submit();
    }
}

function export_campaign() {
    // TODO
}

function go_home() {
    window.location.href = "${attributes['home_path']}";
}

function submit_form() {
    document.getElementById("campaign_form").submit();
}

</script>
</%def>
