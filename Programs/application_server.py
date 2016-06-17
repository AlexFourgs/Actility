#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import client_engine, os, time, logging, logger_initializer, sys
from datetime import datetime
from logging import handlers
from bottle import route, run, request, response, view, static_file
from PyQt4 import QtGui

maximum_data_cookies = 0
list_added = []
data_provider_list = []
graphs_list = []
value_axis_title = ""
list_update = []

#TODO: Add automatic refresh

def start_server(ip_adress, on_port, reloader):
    """Function that starts the server on port 8080"""
    run(host=ip_adress, port=on_port, reloader=reloader)

def reset_cookies():
    """
        This function delete all cookies.
    """
    response.set_cookie("Model", "None", path="/")
    response.set_cookie("Add_button", "true", path="/")
    response.set_cookie("data_list", "", expires=0)
    response.set_cookie("date_from", "", expires=0)
    response.set_cookie("date_to", "", expires=0)
    response.set_cookie("newDataProvider", "", expires=0)
    response.set_cookie("newGraphs", "", expires=0)
    response.set_cookie("submit_refresh", "", expires=0)
    response.set_cookie("auto_refresh", "", expires=0)


    id_number = request.get_cookie("id_number")


    if id_number:
        id_number = int(id_number)
        i = 0
        while (i < id_number):
            cookie_name = "id_" + str(i)
            response.set_cookie(cookie_name, "", expires=0)
            i+=1

        response.set_cookie("id_number", "", expires=0)



    reset_data_cookies()
    #reset_list_cookies()

    response.set_cookie("list_number", "", expires=0)

def reset_data_cookies():
    """
        This function delete the data cookies (the check list of data like temperature, gps...)
    """
    global maximum_data_cookies
    data_number = request.get_cookie("data_number")

    i=0
    while (i < maximum_data_cookies):
        cookie_name = "data_" + str(i)
        response.set_cookie(cookie_name, "", expires=0)
        i+=1

    response.set_cookie("data_number", "", expires=0)

def reset_list_cookies():
    """
        This function delete the data list of cookies that the user add. (Ex : Adeunis 603968382 Temperature between 01/01/2010 00:00:00 and 02/01/2010 00:00:00)
    """
    list_number = request.get_cookie("list_number")

    i=0
    while(i < list_number):
        cookie_name = "list_" + str(i)
        response.set_cookie(cookie_name, "", expires=0)
        i+=1

    response.set_cookie("list_number", "", expires=0)

def init_data_provider(list_value):
    """
        This function create dataProvider that is the value of the JavaScript graph for the data.
        dataProvider is a list of dictionary.

        It is formated like that :
        "dataProvider" : [
            {
                "Date": value,
                "Name_model Id_model": value
            },
            {
                "Date": value,
                "Name_model Id_model": value
                "Name_model Id_model": value
            }
        ]
    """

    global data_provider_list

    for actual_data in list_value: # For every new data
        i=0
        while(i < len(data_provider_list)): # We look over dataProvider.
            if((data_provider_list[i])["date"] == actual_data[1]): #  If there is already a dictionary with the same date.
                (data_provider_list[i])[str(actual_data[2])] = actual_data[0] # We add in this dictionary a new data (ID_Model : Value)
                break
            i+=1

        if(i == len(data_provider_list)): # If there wasn't already a dictionary with actual_data date
            new_date_dictionary = {}
            new_date_dictionary["date"] = str(actual_data[1])
            new_date_dictionary[str(actual_data[2])] = actual_data[0]
            data_provider_list.append(new_date_dictionary)

    response.set_cookie("newDataProvider", "1")

    data_provider_list = sorted(data_provider_list, key=lambda k:k['date'])
    return str(data_provider_list)

def init_graphs(list_value):
    """
        This function create graphs that is the value of the JavaScript graph for the lines.
        graphs is a list of dictionary.

        It is formated like that :
        "graphs" : [
            {
                "key": value,
                "key": value
            },
            {
                "key": value,
                "key": value
                "key": value
            }
        ]
    """
    global graphs_list

    model = list_value[0]
    id_model = list_value[1]

    i=0
    while(i < len(graphs_list)): # We look over graphs
        if((graphs_list[i])["valueField"]==id_model): # If there is already a dictionary with the same ID
            break # We stop the loop
        i+=1

    if(i == len(graphs_list)): # If we didn't find a dictionary in graphs with the same ID
        new_graph = {"balloonText": "Value data of [[category]]: [[value]]", "bullet": "round", "fillAlphas": 0, "hideBulletsCount": 20} # We create it
        new_graph["valueField"] = str(id_model)
        new_graph["title"] = str(model) + " " + str(id_model)
        graphs_list.append(new_graph)

    response.set_cookie("newGraphs", "1")

def submit_add():
    """
        This function is called when the user click on "Add".
        She create all cookies and data (dataProvider, graphs).
    """

    global list_added
    global graphs_list
    global value_axis_title
    global list_update

    # Get data from post request
    dateFrom = request.forms.get("dateFrom").replace('T', ' ')
    model = request.forms.get("model")
    id_model = request.forms.get("ID")
    data = request.forms.get("Data")
    update = request.forms.get("update")
    bool_update = "no"

    if(update != "on"): # If the user doesn't want automatic update of value
        dateTo = request.forms.get("dateTo").replace('T', ' ') # dateTo = Value set by the user
    else:
        bool_update = "yes"
        # dateTo = actual date
        date = time.localtime()
        dateTo = str(date.tm_year) + "-" + str(date.tm_mon) + "-" + str(date.tm_mday) + " " + str(date.tm_hour) + ":" + str(date.tm_min) + ":" + str(date.tm_sec)

        # We save the informations about the charts that we have to updates
        new_value = {"Model":model, "ID":id_model, "data":data, "last_date":dateTo}
        list_update.append(new_value)
        response.set_cookie("auto_refresh", "1", path="/")



    # Set cookies
    list_added.append("%s %s - %s - %s - %s - %s"%(model, id_model, data, dateFrom, dateTo, bool_update))
    response.set_cookie("list_number", str(len(list_added)))

    i=0
    while(i < len(list_added)):
        cookie_name = "list_" + str(i)
        response.set_cookie(cookie_name, list_added[i])
        i+=1


    # Creating data JSON for Javascript
    list_value = engine.get_data_for_graph(model, id_model, data, dateFrom, dateTo) # Get the results list from the database request
    init_data_provider(list_value) # Formalize the list_value in JSON for amGraphs

    list_value_graph = [model, id_model] # Create a list with the id and the model
    init_graphs(list_value_graph) # Formalize the list_value_graph ub JSON for amGraphs

    # Changing the title of axis
    value_axis_title = str(data)

def update_values():
    global list_added
    global list_update

    date = time.localtime()
    dateTo = str(date.tm_year) + "-" + str(date.tm_mon) + "-" + str(date.tm_mday) + " " + str(date.tm_hour) + ":" + str(date.tm_min) + ":" + str(date.tm_sec)

    for actual_data in list_added:
        bool_update = actual_data.split(" - ")[4]
        last_date = actual_data.split(" - ")[3]
        model = actual_data.split(" - ")[0].split(" ")[0]
        id_model = actual_data.split(" - ")[0].split(" ")[1]
        data_in_list = actual_data.split(" - ")[1]
        dateFrom = actual_data.split(" - ")[2]

        if(actual_bool_update == "yes"):
            list_value = engine.get_data_for_graph(model, id_model, data, dateFrom, dateTo)
            data_provider = init_data_provider(list_value)
            #(actual_last_date == last_date) and (actual_model == model) and (actual_id_model == id_model) and (actual_other_data_in_list == data)):
            actual_other_data = "%s %s - %s - %s - %s - %s"%(actual_model, actual_id_model, actual_other_data_in_list, actual_dateFrom, dateTo, actual_bool_update)
    

def submit_del():
    """
        This function deletes data from dataProvider and graphs if necessary.
        When the user select data in the list and click on delete, this function is called.
    """

    global list_added
    global data_provider_list
    global list_update

    # Get the data selected in the list from web page and split it
    data_selected = request.forms.get("list_data_selected")
    splitted_data = data_selected.split(" - ")
    model_and_id = splitted_data[0].split(" ")
    model = model_and_id[0]
    id_model = model_and_id[1]
    data = splitted_data[1]
    date_from = splitted_data[2]
    date_to = splitted_data[3]
    update = splitted_data[4]

    if(update == "yes"): # If it's a data that refresh the page, we remove it from list_update
        for actual_dic in list_update:
            if ((actual_dic["Model"] == model) and (actual_dic["ID"] == id_model) and (actual_dic["data"] == data)):
                list_update.remove(actual_dic)
                break
        if(len(list_update) == 0): # If there are not other data that refresh the page, we set the cookie for desactivate the auto refresh.
            response.set_cookie("auto_refresh", "0", path="/")



    # Remove it from the list
    list_added.remove(data_selected)
    response.set_cookie("list_number", str(len(list_added)))

    # Reset the cookie
    i=0
    while(i < len(list_added)):
        cookie_name = "list_" + str(i)
        response.set_cookie(cookie_name, list_added[i])
        i+=1

    # Reset the dataProvider
    i=0
    while (i < len(data_provider_list)):# We look over the list of dictionary
        actual = data_provider_list[i]
        if(id_model in actual): # If the actual dictionary has the key id_model
            if(len(actual.keys()) == 2): # If there are only 2 keys (date and the id we search)
                actual_date = actual["date"] # Date of actual dictionary
                if((actual_date >= date_from) and (actual_date <= date_to)): # If the date is between the data selected date
                    data_provider_list.remove(actual) # We remove the dictionary from the list of dataProvider
                else:
                    i+=1
            else: # If there are other id with the same date
                actual_date = actual["date"] # Date of actual dictionary
                if((actual_date >= date_from) and (actual_date <= date_to)): # If the date is between the data selected date
                    del actual[id_model] # We remove the id from the actual dictionary
                else:
                    i+=1
        else:
            i+=1

    # Reset the graphs
    id_in_data_provider = [] # List for save every id which have a data in dataProvider
    for actual in data_provider_list: # We look over again the list of dictionary for the id
        for key in actual: # We look over the keys
            if(key != "date"): # We look only for id
                if(key not in id_in_data_provider): # If the id is not in id_in_data_provider
                    id_in_data_provider.append(key) # We add it

    for actual in graphs_list: # We look over graphs_list
        actual_id = actual["valueField"] # ID in graphs
        if(actual_id not in id_in_data_provider): # If there is not data in dataProvider with this id
            graphs_list.remove(actual) # We remove the dictionary from the list of graphs

def submit_model():
    """
        This function is called when the user change the value of the list "Model".
        She call the engine for get the list of ID for the model that the user chose.
        Then, she creates cookies.
    """
    global maximum_data_cookies

    # Set the cookie for the model selectionned and "Add" button
    model = request.forms.get("model")
    response.set_cookie("Model", str(model), path="/")
    response.set_cookie("Add_button", "false", path="/")

    # Set the cookies for the list of id
    list_id = engine.get_id_from_model(model)
    i = 0
    for actual_id in list_id:
        cookie_name = "id_" + str(i)
        response.set_cookie(cookie_name, str(actual_id), path="/")
        i+=1

    response.set_cookie("id_number", str(i), path="/")

    # Set the cookies for the list of data
    list_data = engine.get_data_from_model(model)
    i = 0
    for actual_data in list_data:
        cookie_name = "data_" + str(i)
        response.set_cookie(cookie_name, str(actual_data), path="/")
        i+=1

    response.set_cookie("data_number", str(i), path="/")

    if i > maximum_data_cookies:
        maximum_data_cookies = i


@route('/static/logo_actility')
def image_logo_actility():
    return static_file("logo.png", root="./Images/")

@route('/static/data_viewer_img')
def image_data_viewer():
    return static_file("head.png", root="./Images/")

@route('/static/bg_header')
def image_background_header():
    return static_file("bg_head.jpg", root="./Images/")

@route("/data")
@view("page.tpl")
def set_graph():
    """
        Function called for a simple GET on page /data.
    """
    global data_provider_list
    global graphs_list
    global list_added
    global list_update

    # We delete all data
    del data_provider_list[:]
    del graphs_list[:]
    del list_added[:]
    del list_update[:]
    #cookies = request.cookies()
    #print(cookies.getunicode())
    # We reset / delete all cookies.
    reset_cookies()

    return {"title":"Test", "body":"Je suis le corps de la page html.", "data_provider":"[]", "graphs":"[]", "value_axis_title":""}

@route("/data", method="POST")
@view("page.tpl")
def post_set_graph():
    """
        Function called for a POST on page /data.
    """
    global maximum_data_cookies
    global data_provider_list
    global data_provider
    global graphs_list

    if(request.forms.get("Delete")): # POST from button "Delete"
        submit_del()

    elif(request.forms.get("Add")): # POST from button "Add"
        submit_add()

    else: # POST from JavaScript
        refresh = request.get_cookie("submit_refresh")
        if(refresh == "1"): # Submit for refresh data
            response.set_cookie("submit_refresh", "0", path="/")
            update_values()

        else: # Submit by changing the model
            submit_model()

    return {"title":"Test", "body":"Je suis le body", "data_provider":data_provider_list, "graphs":graphs_list, "value_axis_title":value_axis_title}


@route("/", method="POST")
def listener():
    """
        Method for the listener.
    """
    # curl -X POST --header "Content-Type:application/xml" --data @your_file.xml http://your_server.com:8080/

    if(request.headers['Content-Type'] == "application/xml"):
        file_xml = request.body.read()
        file_path = engine.save_data_file(file_xml)
        engine.general_engine(file_path)
    else :
        logger = logging.getLogger("as_server")
        ip = request.environ.get('REMOTE_ADDR')
        print("Error, it's not a xml file\nFile rejected.\n")
        logger.warning("Class.Server :: listener :: HTTP POST REQUEST received from %s but body isn't a xml file. Rejected."%(ip))
        return "POST Received but not treat, this server is waiting for an xml file."


def window():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    b = QtGui.QLabel(w)
    b.setText("Hello World!")
    w.setGeometry(100,100,200,50)
    b.move(50,20)
    w.setWindowTitle("PyQt")
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    engine = client_engine.Engine()
    #logger_initializer.init_log("as_server", "as_server.log")
    #logging.basicConfig()
    start_server("0.0.0.0", 8080, True)
    #window()
