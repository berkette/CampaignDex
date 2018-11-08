<%namespace name="partials" file="${context['attributes']['partials_filepath']}"/>

<%namespace name="js" file="${context['attributes']['js_filepath']}"/>
<%namespace name="css" file="${context['attributes']['css_filepath']}"/>

<html>
<head>
    ${js.insert()}
    ${css.insert()}
</head>
<body>
    ${partials.header()}
    ${partials.sidebar()}
    
    <div id="main_content">
        <div id="main_content_title">
            <h1>${attributes['title']}</h1>
        </div>
        <div id="main_content_body">
            <button id="edit_button">Edit</button>
            <div id="text_content">
                <p>quill goes here probably</p>
            </div>
        </div>
    </div>
</body>
</html>
