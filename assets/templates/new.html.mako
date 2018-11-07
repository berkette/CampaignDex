<%inherit file="base.html.mako"/>

<%block name="main_content">
    <div id="new_page_form">
        <form action='/save_page' method='post'>
            <label for='page_path'>Relative URL:</label>
            <input type='text' name='page_path' value="${attributes['from_path']}">

            <label for='page_title'>Title:</label>
            <input type='text' name='page_title' value='Title'>

            <label for='page_body'>(Optional) Body:</label>
            <input type='text' name='page_body'>
    
            <input type='submit' value='Create Page'>
        </form>
    </div>
</%block>
