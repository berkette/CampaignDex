<%namespace name="css" file="${context['attributes']['css_filepath']}"/>
<%namespace name="js" file="${context['attributes']['js_filepath']}"/>

<html>
<head>
    ${js.insert()}
    ${css.insert()}
</head>

<body>
    <div id="header">
        <h1>Manage Campaign</h1>
    </div>
    
    <div id="body">
% if 'error' in attributes:
        <div id="errors">
            <p style="color:red;">${attributes['error']}</p>
        </div>
% endif

        <form id="campaign_form" action="${attributes['update_campaign']}" method="post">
            <label for="name">Campaign Name</label>
            <input type="text" name="name" value="${attributes['campaign_name']}"><br>
            <label for="skin">Choose a skin</label>
            <select name="skin">
% for skin in attributes['skins']:
                <option
                    value="${skin}"
    % if skin == attributes['campaign_skin']:
                    selected="selected"
    % endif
                >
                ${skin}
                </option>
% endfor
            </select><br>
            <input type="hidden" name="campaign_id" value="${attributes['campaign_id']}">
        </form>

        <button id="cancel_button" onclick="go_home()">Cancel</button>
        <button id="export_button" onclick="export_campaign()">Export</button>
        <button id="delete_button" onclick="delete_campaign()">Delete</button>
        <button id="submit_button" onclick="submit_form()">Save</button>

    </div>
    <form id="delete_form" action="${attributes['delete_campaign']}" method="post">
        <input type="hidden" name="campaign_id" value="${attributes['campaign_id']}">
    </form>
</body>
</html>
