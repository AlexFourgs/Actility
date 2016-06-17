<!doctype html>
<!-- page.tpl -->
<HTML lang="fr">
  <HEAD>
     <script src="https://www.amcharts.com/lib/3/amcharts.js"></script>
     <script src="https://www.amcharts.com/lib/3/serial.js"></script>
     <script src="https://www.amcharts.com/lib/3/themes/light.js"></script>
     <script src="https://www.amcharts.com/lib/3/plugins/export/export.js" type="text/javascript"></script>
     <link href="https://www.amcharts.com/lib/3/plugins/export/export.css" rel="stylesheet" type="text/css">
     <script src="https://www.amcharts.com/lib/3/ammap.js"></script>
     <script src="https://www.amcharts.com/lib/3/maps/js/worldLow.js"></script>
     <script src="https://www.amcharts.com/lib/3/themes/none.js"></script>


     <title>
       Actility : Data Viewer
     </title>

     <link rel="shortcut icon" href="http://www.actility.com/sites/www.actility.com/files/actility-favicon.png" type="image/png" />
     <!--
     <link rel="stylesheet" href="http://www.actility.com/sites/all/themes/actility/css/bootstrap-responsive.css?o8pfhi" type="text/css" media="screen" />
     <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,400,600,300,700" type="text/css" media="screen" />
     <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Exo:300,400,600" type="text/css" media="screen" />
     <link rel="stylesheet" href="http://www.actility.com/sites/www.actility.com/files/css/css_dWBHPbSQWh-19e3Bc29cTHIsefj--RoEVftmVdOAMn4.css" type="text/css" media="screen" />
     <link rel="stylesheet" href="http://www.actility.com/sites/www.actility.com/files/css/css_fD_6SqndsZKJHz1zENanUJdSS39vsppLQ_SZJoSwKgg.css" type="text/css" media="screen" />
     <link rel="stylesheet" href="http://www.actility.com/sites/www.actility.com/files/css/css_MnXiytJtb186Ydycnpwpw34cuUsHaKc80ey5LiQXhSY.css" type="text/css" media="screen" />
     <link rel="stylesheet" href="http://www.actility.com/sites/www.actility.com/files/css/css_xE-rWrJf-fncB6ztZfd2huxqgxu4WO-qwma6Xer30m4.css" type="text/css" media="screen" />
      -->

     <style>
       html{
         height: 100%;
       }
       header.back{
         background-image: url("http://img11.hostingpics.net/pics/752023bgheader.jpg");
         background-repeat: no-repeat;
         background-position: center top;
         width: 100%;
       }

       img.header{
         position: absolute;
         top: 50%;
       }

       p.indent{
         padding-left: 1.8em
       }
       .center{
         text-align: center
       }
       #chartdiv {
         width : 100%;
         height : 500px;
       }

       select.data_list{
         width: 100%;
         height: 50%;
       }
       aside.onRight{
         width: 15%;
         margin: 0 1.5%;
         float: right;
       }

       section.graphe{
         width: 75%;
         margin: 0 2%;
         float: left;
       }

       p.footerText{
         color:white;
       }
       footer.setBottom{
         background-color: #333333;
         height:200px;
         position: absolute;
         bottom: 0;
         text-align: center;
         width: 100%;
       }

       hr.footer{
         text-align: center;
         width: 75%;
         border-color: #6290B3;
       }

       div.header {
         min-height: 12em;
         display: table-cell;
         vertical-align: middle;
       }


     </style>

     <meta charset="UTF-8">
  </HEAD>

  <body style="min-height:100%; margin:0; padding:0; position:relative; padding-bottom:10em;">
    <header class="back">
      <div class="header">
        <p><div style="width:164px; height:75px; float: left; margin-left:40px;"><a href="http://www.actility.com/" target="_blank"><img style="float:left; width:100%; height:auto;" src="http://www.actility.com/sites/www.actility.com/files/logo2x.png" alt="Logo Actility" /></a></div>
        <img style="margin-left: auto; margin-right: auto;" src="./static/data_viewer_img" alt="Data Viewer" />
        <!--<h1 style="text-align:center; float:right; color:white; font-family: Verdana; font-size:40px;">Data Viewer</h1>--></p>
      </div>

    </header>
    <br/>
    <hr/>

    <form class="center" method="post" action="./data" id="form_graph">
      From : <input type="datetime-local" min="2010-01-01T00:00:00" step=1 value="2010-01-01T00:00:00" name="dateFrom" id="dateFrom"/>
      To : <input type="datetime-local" min="2010-01-01T00:00:00" step=1 name="dateTo" id="dateTo"/>
      <label for="update">Auto refresh : </label><input type="checkbox" name="update" id="update"/>
      Model : <select name="model" id="model"><option value="None" selected></option><option value="Adeunis">Adeunis</option><option value="Watteco">Watteco</option></select>
      ID : <select name="ID" id="ID"><option value="None" selected>Please select a model</option></select>
      Data : <select name="Data" id="Data"><option value="None" selected>Please select a model</option></select>
      <input id="Add" type="submit" name="Add" value="Add" disabled="disabled">
    </form>

    <hr/>
    <p>

      <section class="graphe">
        <div id="chartdiv"></div>
      </section>

      <!--
      <section class="graphe">
        <div id="mapdiv"></div>
      </section>
      -->

      <aside class="onRight">
        <form method="post" action="./data" id="list_box">
          <select class="data_list" name="list_data_selected" size="25" id="list_data_selected">
          </select>
          <br/>
          <div class="center"><input id="Delete" type="submit" name="Delete" value="Delete" disabled="disabled"></div>
        </form>
      </aside>

      <div class="clear" style="clear:both"></div>

      <footer class="setBottom">
        <p>
          <a href="http://store.thingpark.com/" target="_blank"><img src="http://www.actility.com/sites/www.actility.com/files/styles/blanc/public/logo/store.png?itok=_UNzd_Vg" alt="Logo Actility" /></a>
          <a href="http://www.thingpark.com/" target="_blank"><img src="http://www.actility.com/sites/www.actility.com/files/styles/blanc/public/logo/tp.png?itok=IYXxKCyf" alt="Logo Actility" /></a>
          <a href="http://www.energy.actility.com/" target="_blank"><img src="http://www.actility.com/sites/www.actility.com/files/styles/blanc/public/logo/energy_0.png?itok=rgpIuZC_" alt="Logo Actility" /></a>
          <a href="http://partner.thingpark.com/" target="_blank"><img src="http://www.actility.com/sites/www.actility.com/files/styles/blanc/public/logo/dev2.png?itok=1N6GRRZO" alt="Logo Actility" /></a>
        </p>
        <hr class="footer"/>
        <p class="footerText"><font size="-1"><i>Page réalisée par <a href="https://www.linkedin.com/in/alexandre-fourgs-14323711a" target="_blank">Alexandre Fourgs</a> pour Actility.</i></font></p>
      </footer>

      <p hidden style="display:none;" id="data_provider">{{data_provider}}</p>
      <p hidden style="display:none;" id="graphs">{{graphs}}</p>
      <p hidden style:"display:none;" id="value_axis_title">{{value_axis_title}}</p>
    </p>

    <script charset="UTF-8">
      // form document
      var form = document.getElementById("form_graph");

      // We create a variable for survey the list and a event listener
      var model_list = document.getElementById("model");
      var id_list = document.getElementById("ID");
      var data_list = document.getElementById("Data");
      var date_from = document.getElementById("dateFrom");
      var date_to = document.getElementById("dateTo");
      var list_box = document.getElementById("list_data_selected");
      var delete_button = document.getElementById("Delete");
      var add_button = document.getElementById("Add");
      var checkbox = document.getElementById("update");

      var data_provider_text = document.getElementById("data_provider").innerText.replace(/'/g, '"');
      var graphs_text = document.getElementById("graphs").innerText.replace(/'/g, '"');
      var value_axis_title = document.getElementById("value_axis_title").innerText ;

      var data_provider_json = JSON.parse(data_provider_text);
      var graphs_json = JSON.parse(graphs_text);

      // We initialize the max date of the form with the current date
      date_from.setAttribute("max", get_current_date());
      date_to.setAttribute("max", get_current_date());

      /**

        Events

      **/
      // With the listener here, if the value of model's list change, we generate the list "ID" and "Data"
      model_list.addEventListener('change', function() {
        generate_id_list(model_list.options[model_list.selectedIndex].innerHTML);
      });

      // This listener enable the delete button if an item is selectionned in the list box and save his value in a cookie.
      list_box.addEventListener('change', function() {
        if(typeof list_box.options[list_box.selectedIndex].text !== undefined){
          delete_button.disabled = false ;
        }
      });

      data_list.addEventListener('change', function(){
        document.cookie = "data_list=" + list_box.value ;
      });

      // This listener save in a cookie the value of the id_list if it changes.
      id_list.addEventListener('change', function() {
        document.cookie = "id_list=" + id_list.value ;
      });

      date_to.oninput = function(){date_to_cookie()};
      date_from.oninput = function(){date_from_cookie()};
      checkbox.onchange = function(){update_selected()};

      /**
        initialize every parameters
      **/

      initialize_value();

      /**
        For refresh data.
      **/

      if(getCookie("auto_refresh")!= "None"){
        if(getCookie("auto_refresh") == 1){
          setIntervale(refresh_data(), 60000);
        }
      }
      /**
        Functions.
      **/

      // This function check the cookies for set the values in the form.
      function initialize_value(){
        if(getCookie("data_list")!=""){
          list_box.value = getCookie("data_list");
        }

        if(getCookie("id_list")!=""){
          id_list.value = getCookie("id_list");
        }

        if(getCookie("Model")!="None"){
          model_list.value=getCookie("Model");
          init_id_list();
          init_data_list();
        }

        if(getCookie("list_number")!=""){
          list_box.innerHTML = ""
          list_number = parseInt(getCookie("list_number"));

          var i = 0 ;
          while(i < list_number){
            str_actual_list = "list_" + parseInt(i);
            actual_in_list = getCookie(str_actual_list);
            list_box.innerHTML += "<option value=" + actual_in_list + ">" + actual_in_list + "</option>" ;
            i++ ;
          }
        }

        if(getCookie("date_to")!=""){
            date_to.value = getCookie("date_to");
        }
        else {
            date_to.setAttribute("value", get_current_date());
        }

        if(getCookie("date_from")!=""){
          date_from.value = getCookie("date_from");
        }

        if(getCookie("Add_button")=="false"){
          add_button.disabled = false ;
        }
      }

      // Function that save the value of the date_to
      function date_to_cookie(){
        document.cookie = "date_to=" + date_to.value ;
      }

      // Function that save the value of the date_to
      function date_from_cookie(){
        document.cookie = "date_from=" + date_from.value ;
      }

      // Function that disabled the date_to object.
      function update_selected(){
        if(checkbox.checked){
          date_to.disabled = true ;
        }
        else{
          date_to.disabled = false ;
        }
      }

      // Function for initialize the id's list.
      function init_id_list(){
        id_list.innerHTML = ""
        var i = 0 ;
        id_number = parseInt(getCookie("id_number"));
        if(id_number!=0){
          while (i < id_number) {
            str_actual_id = "id_" + parseInt(i);
            actual_id = getCookie(str_actual_id);
            id_list.innerHTML += "<option value=" + actual_id + ">" + actual_id + "</option>" ;
            i++;
          }
        }
      }

      // Function for initialize the data's list.
      function init_data_list(){
        data_list.innerHTML = "";
        var i = 0 ;
        data_number = parseInt(getCookie("data_number"));
        if(data_number!=0){
          while (i < data_number) {
            str_actual_data = "data_" + parseInt(i);
            actual_data = getCookie(str_actual_data);
            data_list.innerHTML += "<option value=" + actual_data + ">" + actual_data + "</option>" ;
            i++;
          }
        }
      }

      // Function to get a cookie.
      function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i = 0; i <ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length,c.length);
            }
        }
        return "";
      }

      // Function that generate id and data list
      function generate_id_list(model){
        if(model=="Adeunis"){
          form.submit();
        }
        else if (model=="Watteco") {
          form.submit();
        }
        else{
          alert("Nothing selectionned");
        }
      }

      function refresh_data(){
        document.cookie = "submit_refresh=1" ;
        form.submit();
      }

      // Function to get the current date to the format YYYY-MM-DDTHH:mm:SS
      function get_current_date(){
        var today = new Date();
        var year = parseInt(today.getFullYear());
        var month = parseInt(today.getMonth()+1) ;
        var day = parseInt(today.getDate());
        var hour = parseInt(today.getHours());
        var minute = parseInt(today.getMinutes());
        var second = parseInt(today.getSeconds());

        if(month < 10){
          month = "0" + month ;
        }

        if(day < 10){
          day = "0" + day ;
        }

        if(hour < 10){
          hour = "0" + hour ;
        }

        if(minute < 10){
          minute = "0" + minute ;
        }

        if(second < 10){
          second = "0" + second ;
        }

        var date = year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second ;

        return date ;
      }

      // Graphe
      var json_graph = {
        "type": "serial",
        "theme": "light",
        "legend": {
            "useGraphSettings": true
        },
        "dataProvider": data_provider_json,
        "valueAxes": [{
            "integersOnly": true,
            "reversed": false,
            "axisAlpha": 0,
            "dashLength": 5,
            "gridCount": 30,
            "position": "left",
            "title": value_axis_title
        }],
        "startDuration": 0.5,
        "graphs": graphs_json,
        "chartCursor": {
            "cursorAlpha": 0,
            "zoomable": false
        },
        "categoryField": "date",
        "categoryAxis": {
            "dashLength": 0,
            "dateFormats": [
              {
                "period": "fff",
                "format": "YYYY-MM-DD JJ:NN:SS"
              },
              {
                "period": "ss",
                "format": "YYYY-MM-DD JJ:NN:SS"
              },
              {
                "period": "mm",
                "format": "YYYY-MM-DD JJ:NN:SS"
              },
              {
                "period": "hh",
                "format": "YYYY-MM-DD JJ:NN:SS"
              },
              {
                "period": "DD",
                "format": "YYYY-MM-DD JJ:NN:SS"
              },
              {
                "period": "WW",
                "format": "YYYY-MM-DD JJ:NN:SS"
              },
              {
                "period": "MM",
                "format": "YYYY-MM-DD JJ:NN:SS"
              },
              {
                "period": "YYYY",
                "format": "YYYY-MM-DD JJ:NN:SS"
              }
            ],
            "title":"Date",
            "gridPosition": "start",
            "axisAlpha": 0,
            "fillAlpha": 0.05,
            "fillColor": "#000000",
            "gridAlpha": 0,
            "position": "bottom",
            "labelRotation": -30
        },
        "mouseWheelZoomEnabled": true,
        "chartScrollbar": {
          "autoGridCount": true,
          "scrollbarHeight": 20
        },
        "export": {
          "enabled": true,
          "position": "bottom-right"
         }
      };

      var targetSVG = "M9,0C4.029,0,0,4.029,0,9s4.029,9,9,9s9-4.029,9-9S13.971,0,9,0z M9,15.93 c-3.83,0-6.93-3.1-6.93-6.93S5.17,2.07,9,2.07s6.93,3.1,6.93,6.93S12.83,15.93,9,15.93 M12.5,9c0,1.933-1.567,3.5-3.5,3.5S5.5,10.933,5.5,9S7.067,5.5,9,5.5 S12.5,7.067,12.5,9z";

      json_map = {
        type: "map",
        "projection":"winkel3",
        "theme": "none",
        imagesSettings: {
          rollOverColor: "#089282",
          rollOverScale: 3,
          selectedScale: 3,
          selectedColor: "#089282",
          color: "#13564e"
        },
        areasSettings: {
          unlistedAreasColor: "#15A892",
          outlineThickness:0.1
        },
        dataProvider: {
          map: "worldLow",
          images: [ {
            svgPath: targetSVG,
            zoomLevel: 5,
            scale: 0.5,
            title: "Vienna",
            latitude: 48.2092,
            longitude: 16.3728
          },
          {
            svgPath: targetSVG,
            zoomLevel: 5,
            scale: 0.5,
            title: "Tunis",
            latitude: 36.8117,
            longitude: 10.1761
          } ]
        },
        "export": {
          "enabled": true
        }
      };

      var chart = AmCharts.makeChart("chartdiv", json_graph);
      window.map = AmCharts.makeChart("mapdiv", json_map);

    </script>
  </body>
</HTML>
