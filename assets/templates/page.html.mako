<%namespace name="partials" file="${context['attributes']['partials_filepath']}"/>
<%namespace name="js" file="${context['attributes']['js_filepath']}"/>
<%namespace name="css" file="${context['attributes']['css_filepath']}"/>

<html>
<head>
    ${partials.scripts(True)}
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
            <button id="edit_button" onclick="edit_page()">Edit</button>
            <div id="quill_editor"></div>
        </div>
    </div>
    
    <form id="quicklink_form" action="${attributes['toggle_quicklink']}" method="post">
        <input type="hidden" name="path" value="${attributes['page_path']}">
        <input type="hidden" name="quicklink" value="${attributes['quicklink']}">
    </form>

    <script>
        initialize_quill(false);
        get_rtf_content();
    </script>
</body>
</html>
