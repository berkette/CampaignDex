<%namespace name="css" file="${context['attributes']['css_filepath']}"/>
<%namespace name="js" file="${context['attributes']['js_filepath']}"/>

<html>
<head>
    ${js.insert()}
    ${css.insert()}
</head>

<body>
    <div id="header">
        <h1>CampaignDex</h1>
        <h2>New</h2>
    </div>
    
    <div id="body">
% if 'error' in attributes:
        <div id="errors">
            <p style="color:red;">${attributes['error']}</p>
        </div>
% endif

        <form id="campaign_form" action="${attributes['save_campaign']}" method="post">
            <label for="name">Name Campaign:</label>
            <br>
            <input type="text" name="name" placeholder="New Name" value="${attributes['name']}">
            <br><br>
            <label for="skin">Choose a Skin:</label>
            <br>
            <select name="skin">
% for skin in attributes['skins']:
                <option value="${skin}">${skin}</option>
% endfor
            </select><br>
        </form>

        <button id="cancel_button" onclick="go_home()">Cancel</button>
        <button id="submit_button" onclick="submit_form()">Start</button>

    </div>
</body>
</html>
