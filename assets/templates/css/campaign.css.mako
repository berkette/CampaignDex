<%def name="insert()">
<style>
body {
    background-image: url("/images/hexellence.png");
    color: #191B1D;
    font-family: "Arial", sans-serif;
    margin: 0;
    text-align: center;
}

#header {
    background-color: #191B1D;
    background-image: url("/images/binding_dark.png");
    height: 150px;
    left: 0px;
    position: absolute;
    top: 0px;
    width: 100%;
    z-index: 10;
}

h1 {
    color: white;
    display: inline-block;
    font-family: "Arial Black", sans-serif;
    font-size: 60px;
    line-height: 100px;
    margin: 0;
    text-align: center;
    vertical-align: middle;
    width: 100%;
}

h2 {
    color: white;
    display: inline-block;
    font-family: "Arial", sans-serif;
    font-size: 30px;
    line-height: 30px;
    margin: 0;
    text-align: center;
    vertical-align: middle;
    width: 100%;
}

#body {
    background-color: white;
    display: inline-block;
    max-width: 800px;
    padding-bottom: 50px;
    padding-top: 170px;
    position: relative;
    text-align: center;
    width: 100%;
    z-index: 5;
}

button {
    background-color: #191B1D;
    border: none;
    color: white;
    display: inline-block;
    font-family: "Arial Black", sans-serif;
    font-size: 16px;
    height: 36px;
    line-height: 36px;
    padding: 0 20px;
    vertical-align: middle;
}

#campaign_list {
    border: 1px solid #191B1D;
    display: inline-block;
    height: 40vh;
    min-height: 200px;
    overflow: scroll;
    width: 600px;
}

#campaign_table {
    padding: 0;
    width: 100%;
}

#campaign_table td {
    height: 30px;
    padding: 0;
    text-align: center;
    width: 100%;
}

#campaign_table td:hover {
    background-color: #E1E8EF;
}

#campaign_table tr:nth-child(even) {
    background-color: #CAD6E2;
}

#campaign_table .campaign {
    height: 30px;
    line-height: 30px;
    vertical-align: middle;
}

label, input {
    height: 30px;
    line-height: 30px;
    font-size: 16px;
    text-align: center;
    vertical-align: middle;
    width: 600px;
}

select {
    height: 30px;
    font-size: 16px;
}

#errors {
    background-color: #E1E8EF;
    display: inline-block;
    padding: 10px 0;
    width: 600px;
}

</style>
</%def>
