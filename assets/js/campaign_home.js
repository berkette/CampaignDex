var selected_campaign = '';
var selected_div_id = '';

function select_campaign(div_id, campaign_id) {
    if (selected_div_id != '') {
        document.getElementById(selected_div_id).style.backgroundColor = "initial";
    }
    selected_campaign = campaign_id;
    selected_div_id = div_id;
    document.getElementById(div_id).style.backgroundColor = "lightblue";
    document.getElementById("open_button").disabled = false;
    document.getElementById("manage_button").disabled = false;
}

function open_campaign() {
    document.getElementById("open_hidden").value = selected_campaign;
    document.getElementById("open_form").submit();
}

function manage_campaign() {
    document.getElementById("manage_hidden").value = selected_campaign;
    document.getElementById("manage_form").submit();
}
