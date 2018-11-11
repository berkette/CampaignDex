<%namespace name="partials" file="${context['attributes']['partials_filepath']}"/>
<%namespace name="js" file="${context['attributes']['js_filepath']}"/>
<%namespace name="css" file="${context['attributes']['css_filepath']}"/>

<html>
<head>
    ${partials.scripts(False)}
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
            <button class="cd_button" id="delete_button" onclick="delete_page()">Delete</button>
            <button class="cd_button" id="save_button" onclick="submit_form()">Save</button>
            <button class="cd_button" id="cancel_button" onclick="go_to_view()">Cancel</button>
        </div>

        <div id="main_content_body">
% if 'error' in attributes:
            <div id="errors">
                <p style="color:red;">${attributes['error']}</p>
            </div>
% endif
            <form class="cd_form" id="page_form" action="${attributes['save_page']}" method="post">
                <label for="page_path">Relative URL:</label>
                <br>
                <input type="text" name="page_path" value="${attributes['page_path_value']}">
                <br>
                <label for="page_title">Title:</label>
                <br>
                <input type="text" name="page_title" value="${attributes['title']}">
                <input type="hidden" name="original_path" value="${attributes['page_path']}">
            </form>
            <button class="cd_button" id="form_button" onclick="submit_form()">Save Changes</button>
        </div>
    </div>

    <form class="cd_form" id="delete_form" action="${attributes['delete_page']}" method="post">
        <input type="hidden" name="path" value="${attributes['page_path']}">
    </form>
</body>
</html>
