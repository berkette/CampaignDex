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
            <h1>${attributes['title']}</h1>
        </div>
        <div id="main_content_body">
            <button id="save_button" onclick="save_page(false)">Save</button>
            <button id="apply_button" onclick="save_page(true)">Apply</button>
            <div id="quill_editor"></div>
        </div>
    </div>

    <form id="save_form" method="post">
        <input type="hidden" name="path" value="${attributes['page_path']}">
        <input id="save_hidden" type="hidden" name="rtf">
    </form>

    <script>
        initialize_quill(true);
        get_rtf_content();
    </script>
</body>
</html>