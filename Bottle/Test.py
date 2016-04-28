#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

# Premier test de bottle.

from bottle import route, run, template, request

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
    @route(url, method="GET")
    def lel():
        return "Nothing"


run(host='0.0.0.0', port=8080, debug=True)
