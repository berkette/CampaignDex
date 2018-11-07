<%inherit file="base.html.mako"/>

<%block name="main_content">
    <div id="superpage">Up</div>
    <div id="quicklink">Add to Quicklinks</div>
    ${parent.main_content()}
</%block>
