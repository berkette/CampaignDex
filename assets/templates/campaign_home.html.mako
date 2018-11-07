<%namespace name="js" file="${context['attributes']['js_filepath']}"/>
<%namespace name="css" file="${context['attributes']['css_filepath']}"/>

<html>
<head>
    ${js.insert()}
    ${css.insert()}
</head>

<body>
    <div id="header">
        <h1>CampaignDex</h1>
        <h2>Home</h2>
    </div>

    <div id="body">
        <button id="new_button" onclick="new_campaign()">Start a New Campaign</button>
        <p>or</p>
        <div id="campaign_list">
            <table id="campaign_table">
% for campaign in attributes['campaigns']:
            
                <tr><td><div
                    class="campaign"
                    id="campaign_${campaign.id}"
                    onclick="select_campaign('campaign_${campaign.id}','${campaign.id}')"
                >
                    ${campaign.name}
                </div></td></tr>
% endfor
            </table>
        </div>
        <br>
        <button id="open_button" onclick="open_campaign()" disabled>Open</button>    
        <button id="manage_button" onclick="manage_campaign()" disabled>Manage</button>
        <form id="open_form" action="${attributes['open_campaign']}" method="post">
            <input id="open_hidden" type="hidden" name="campaign"></input>
        </form>
    </div>
</body>
</html>
