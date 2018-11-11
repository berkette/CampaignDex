<%def name="insert()">
<style>

@keyframes sidebar_slide {
    from {left: -180px;}
    to {left: 0px;}
}

body {
    background-image: url("/images/hexellence.png");
    color: #191B1D;
    font-family: "Arial", sans-serif;
    margin: 0;
    text-align: center;
}

.cd_button {
    background-color: #191B1D;
    border: none;
    color: white;
    display: inline-block;
    font-family: "Arial Black", sans-serif;
    font-size: 16px;
    height: 36px;
    line-height: 36px;
    margin: 0;
    text-align: center;
    vertical-align: middle;
}

.cd_h1 {
    display: inline-block;
    font-family: "Arial Black", sans-serif;
    margin: 0;
    text-align: center;
    vertical-align: middle;
}

##### Header #####

#header {
    background-color: #191B1D;
    background-image: url("/images/binding_dark.png");
    box-shadow: 0px 0px 7px black;
    color: white;
    height: 50px;
    left: 0px;
    min-width: 800px;
    position: absolute;
    text-align: center;
    top: 0px;
    width: 100%;
    z-index: 10;
}

#header .cd_button {
    background-color: transparent;
    height: inherit;
    line-height: 50px;
    position: absolute;
    vertical-align: middle;
    width: 200px;
    z-index: 12;
}

#header .cd_h1 {
    font-size: 24px;
    height: inherit;
    line-height: 50px;
    margin: 0 -25%;
    padding: 0;
    position: absolute;
    width: 50%;
    z-index: 11;
}

#header_exit_button {
    left: 0px;
}

#header_new_button {
    right: 0px;
}


##### Sidebar #####

#sidebar {
    background-color: #191B1D;
    background-image: url("/images/binding_dark.png");
    box-shadow: 0px 0px 7px black;
    color: white;
    height: 80vh;
    left: -180px;
    overflow: scroll;
    position: fixed;
    text-align: center;
    top: 10vh;
    width: 200px;
    z-index: 5;
}

#sidebar:hover {
    left: 0px;
}

#sidebar_content {
    height: inherit;
    position: absolute;
    top: 0px;
    left: 0px;
    width: 180px;
}

#sidebar_handle {
    height: inherit;
    position: absolute;
    top: 0px;
    left: 180px;
    width: 20px;
}

#sidebar_home_button {
    background-image: url("/images/binding_dark.png");
    display: block;
    font-size: 24px;
    height: 50px;
    left: 0px;
    line-height: 50px;
    position: relative;
    top: 20px;
    width: 100%;
}

#path_links {
    border-top: 1px solid grey;
    display: inline-block;
    position: relative;
    top: 20px;
    width: 150px;
}

#subpages {
    border-top: 1px solid grey;
    display: inline-block;
    margin-top: 15px;
    position: relative;
    top: 20px;
    width: 150px;
}

#quicklinks {
    border-top: 1px solid grey;
    display: inline-block;
    margin-top: 15px;
    position: relative;
    top: 20px;
    width: 150px;
}

#sidebar .cd_ul {
    position: relative;
    list-style-image: url("/images/right_bracket.png");
    list-style-position: inside;
    margin: 0;
    margin-left: 10px;
    padding: 0;
    text-align: left;
}

#sidebar a {
    color: white;
    text-decoration: none;
}

##### Main Content #####

#main_content {
    background-color: white;
    box-sizing: border-box;
    display: inline-flex;
    flex-direction: column;
    min-height: 100vh;
    padding-bottom: 50px;
    text-align: center;
    width: 800px;
    z-index: 1;
}

#main_content_title, #main_content_buttons {
    display: inline-block;
    height: 50px;
    line-height: 50px;
    position: relative;
    vertical-align: middle;
    width: 100%;
}

#main_content_title {
    margin-top: 70px;
}

#main_content_buttons .cd_button {
    display: inline-block;
    position: relative;
    width: 170px;
    z-index: 3;
}

#main_content_body {
    box-sizing: border-box;
    display: inline-block;
    flex-grow: 1;
    position: relative;
    left: 50px;
    width: 700px;
    z-index: 2;
}

</style>
</%def>