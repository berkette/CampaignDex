<%namespace name="js" file="${context['attributes']['js_filepath']}"/>
<%namespace name="css" file="${context['attributes']['css_filepath']}"/>

<html>
<head>
    ${js.insert()}
    ${css.insert()}
</head>

<body>
    <div id="header">
        <h1>Welcome to CampaignDex</h1>
    </div>

    <div id="body">
        <button id="new_button" onclick="new_campaign()">Start a New Campaign</button>
        <p>or</p>
        <div id="campaign_list">
% for campaign in attributes['campaigns']:
            <div
                class="campaign"
                id="campaign_${campaign.id}"
                onclick="select_campaign('campaign_${campaign.id}','${campaign.id}')"
            >
                ${campaign.name}
            </div>
% endfor
        </div>
        <button id="open_button" onclick="open_campaign()" disabled>Open</button>    
        <button id="manage_button" onclick="manage_campaign()" disabled>Manage</button>
        <form id="open_form" action="${attributes['open_campaign']}" method="post">
            <input id="open_hidden" type="hidden" name="campaign"></input>
        </form>
    </div>
</body>
</html>
