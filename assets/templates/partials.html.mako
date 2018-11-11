<%def name="scripts(include_quill)">
    <script src="${attributes['jquery_js']}"></script>
    % if include_quill == True:
    <link href="${attributes['quill_snow']}" rel="stylesheet">
    <script src="${attributes['quill_js']}"></script>
    % endif
</%def>

<%def name="header()">
    <div id="header">
        <button class="cd_button" id="header_exit_button" onclick="exit_campaign()">
            Exit Campaign
        </button>
        <h1 class="cd_h1" onclick="go_to_home()">${attributes['campaign_name']}</h1>
        <button class="cd_button" id="header_new_button" onclick="go_to_new()">New Page</button>
    </div>
</%def>

<%def name="sidebar()">
    <div id="sidebar">
        <div id="sidebar_content">
            <button class="cd_button" id="sidebar_home_button" onclick="go_to_home()">Home</button>

            <div id="path_links">
                <h3>Path</h3>
                ${_nested_ul(attributes['path_links'])}
            </div>

            <div id="subpages">
                <h3>Subpages</h3>
                <ul class="cd_ul">
    % for subpage in attributes['subpages']:
                    <li class="cd_li"><a href="${subpage['path']}">${subpage['title']}</a></li>
    % endfor
                    <li class="cd_li" onclick="go_to_new()">New Subpage</li>
                </ul>
            </div>

            <div id="quicklinks">
                <h3>Quicklinks</h3>
                <ul class="cd_ul">
    % for quicklink in attributes['quicklinks']:
                    <li class="cd_li"><a href="${quicklink['path']}">${quicklink['title']}</a></li>
    % endfor
                </ul>
            </div>
        </div>
        <div id="sidebar_handle"></div>
    </div>
</%def>


###### Private ######

<%def name="_nested_ul(path_links)">
    % if len(path_links) > 0:
        <ul class="cd_ul"><li class="cd_li">
            <a href="${path_links[0]['path']}">${path_links[0]['basename']}</a>
            ${_nested_ul(path_links[1:])}
        </li></ul>
    % endif
</%def>
