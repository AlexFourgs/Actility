#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

# Premier test de bottle.
from function import save_data
from bottle import route, run, template, request, response, redirect

# Decorator
@route('/hello')
def hello():
    return "<h1>Hello World !</h1>"

@route('/test')
def test():
    return "This is a test !"

# Test URL dynamique.
@route('/hello/<name>')
def hello_name(name='Stranger'):
    return template('Hello {{name}}, how are you ?', name=name)

# Test formulaire.
@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

# Permet de récupérer les données d'un POST.
# Adapter
@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

def check_login(username, password):

    if (username == 'Test') and (password == 'test'):
        return True
    else:
        return False


# Test formulaire + méthode GET
@route("/form_get")
def form_get():
    # Code HTML
    return '''
        <form action="/form_get" method="post">
            Site: <input name="url" type="text" />
            <input value="Login" type="submit" />
        </form>
    '''

@route("/form_get", method="POST")
def do_form_get():
    url = request.forms.get("url")
    @route(url)
    def lel():
        return "Nothing"

# Test récolte de donnée dans l'URL
@route("/test_data_url")
def url_get_data():
    # Aller à l'URL "localhost:8080/test_data_url?id=30" par exemple
    id_test = request.query.id

    return template("ID = {{id_url}}", id_url=id_test)


# Test récolte donnée envoyer par un POST par cURL
@route("test_post/:file_xml", method="POST")
def post_get_data(file_xml):
    data = file_xml
    print data
    ## Vérifier d'où provient le POST
    ## Enregistrer la donnée.

# Permet de rediriger vers une autre URL.
@route("/redirect")
def redirect_to_google():
    redirect("http://google.com")


# Permet de récupérer les fichiers XML via protocole HTTP "POST" et affiche le contenu du fichier.
@route("/listener", method="POST")
def recolt_xml():
    if request.headers['Content-Type'] == "text/xml":
        file_xml = request.body.read()
        save_data(file_xml)
        return "This is an xml file !\nXML FILE : " + file_xml
    else :
        return "Error, it's not a xml file\n"


run(host='0.0.0.0', port=80, debug=True)
