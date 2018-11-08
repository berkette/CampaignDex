<%namespace name="partials" file="${context['attributes']['partials_filepath']}"/>

<%namespace name="js" file="${context['attributes']['js_filepath']}"/>
<%namespace name="css" file="${context['attributes']['css_filepath']}"/>

<html>
<head>
    <link href="${attributes['quill_snow']}" rel="stylesheet">
    <script src="${attributes['quill_js']}"></script>

    ${js.insert()}
    ${css.insert()}
</head>
<body>
    ${partials.header()}
    ${partials.sidebar()}
    
    <div id="main_content">
        <button id="superpage_button" onclick="go_to_superpage()">Up</button>
        <button id="quicklink_button" onclick="toggle_quicklink()">
% if attributes['quicklink'] == True:
            Remove Quicklink
% else:
            Add Quicklink
% endif
        </button>
        <div id="main_content_title">
            <h1>${attributes['title']}</h1>
        </div>
        <div id="main_content_body">
            <button id="save_button" onclick="save_page(false)">Save</button>
            <button id="apply_button" onclick="save_page(true)">Apply</button>
            <div id="quill_editor"></div>
        </div>
    </div>

    <form id="quicklink_form" action="${attributes['toggle_quicklink']}" method="post">
        <input type="hidden" name="path" value="${attributes['page_path']}">
        <input type="hidden" name="quicklink" value="${attributes['quicklink']}">
    </form>

    <form id="save_form" method="post">
        <input type="hidden" name="path" value="${attributes['page_path']}">
        <input id="save_hidden" type="hidden" name="rtf">
    </form>
    
    <script>
        initialize_quill(true);
        populate_page();
    </script>
</body>
</html>
