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
        <div id="main_content_title">
            <h1 class="cd_h1">${attributes['title']}</h1>
        </div>

        <div id="main_content_buttons">
            <button class="cd_button" id="superpage_button" onclick="go_to_superpage()">Up</button>
            <button class="cd_button" id="manage_button" onclick="go_to_manage()">Manage</button>
            <button class="cd_button" id="edit_button" onclick="go_to_edit()">Edit</button>
            <button class="cd_button" id="quicklink_button" onclick="toggle_quicklink()">
% if attributes['quicklink'] == True:
                Remove Quicklink
% else:
                Add Quicklink
% endif
            </button>
        </div>

        <div id="main_content_body">
            <div id="quill_editor"></div>
        </div>
    </div>
    
    <form class="cd_form" id="quicklink_form" action="${attributes['toggle_quicklink']}" method="post">
        <input type="hidden" name="path" value="${attributes['page_path']}">
        <input type="hidden" name="quicklink" value="${attributes['quicklink']}">
    </form>

    <script>
        initialize_quill(false);
        get_rtf_content();
    </script>
</body>
</html>
