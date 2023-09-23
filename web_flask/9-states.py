#!/usr/bin/python3
""" start web app """

from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """ Display a list of states """
    state_objects = storage.all('State').values()
    states = sorted(state_objects, key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """ Display cities of a specific state """
    state_objects = storage.all('State').values()
    states = sorted(state_objects, key=lambda state: state.name)
    for state in states:
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html', not_found=True)


@app.teardown_appcontext
def teardown(exception):
    """ remove sql session """
    storage.close()


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port='5000', debug=True)
