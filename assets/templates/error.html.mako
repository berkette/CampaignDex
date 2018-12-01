<%namespace name="css" file="${context['attributes']['css_filepath']}"/>

<html>
<head>
    ${css.insert()}
</head>

<body>
    <div id="header">
        <h1>CampaignDex</h1>
        <h2>Internal Server Error</h2>
    </div>

    <div id="body">
        <p>${attributes['error']}</p>
    </div>
</body>
</html>