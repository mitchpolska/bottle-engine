from bottle import route, run, template, request
from jinja2 import Environment, PackageLoader
from tornado import web, ioloop
from pymongo import Connection
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import datetime

@route('/register.html', method=['GET', 'POST'])
def register():
    form = RegistrationForm(request.POST)
    userExists = False
    if request.method == 'POST' and form.validate():
        connection = Connection()
        db = connection.test_database
        users = db.users
        userExists = users.find_one({'email' : str(form.email.data)})
        if not userExists:
            user = {'_id':users.count(),
                    'email' : str(form.email.data),
                    'password' : str(form.password.data)}
            users.insert(user)
        else:
            form.email.errors = {"User exists 2"}
            
    template = env.get_template('index.html')
    return template.render(form=form)

@route('/')
def index():
    return 'INDEX'
    
class RegistrationForm(Form):
    email        = TextField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password     = PasswordField('Password', [validators.Length(min=4, max=25)])
    accept_rules = BooleanField('I accept the site rules', [validators.Required()])
    
env = Environment(loader=PackageLoader('bottle', 'views'))    
run(host='bottle.dev', port=8080, server='tornado', debug=True, reloader=True)
