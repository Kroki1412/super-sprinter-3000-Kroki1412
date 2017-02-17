# The extensive comments are for myself as I am new to flask and it helps with code purpose.
# all the imports
import os
from peewee import *
from flaskr.connectdatabase import ConnectDatabase
from flaskr.models import Entries
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app


app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py


if __name__ == "__main__":
    app.run()

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='kroki',
    PASSWORD='test123'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([Entries], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


#---------------------------------------

# base webpage
@app.route('/')
def show_entries():
    entries = Entries.select().order_by(Entries.id.desc())
    return render_template('show_entries.html', entries=entries)


# add this part will add a user story
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    new_entry = Entries.create(title=request.form['title'],
                               text=request.form['text'])
    new_entry.save()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


# this part will log in the user
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(app.config['USERNAME'])
    print(app.config['PASSWORD'])
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


# this part hadels the logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# this part handels the listing
@app.route('/list' methods=['GET'])
def listing():
    entries = Entries.select().order_by(Entries.id.desc())
    return render_template('list.html', entries=entries)


# this part handels the editing of the page
@app.route('/edit' methods=['GET', 'UPDATE'])
def listing():
    return
