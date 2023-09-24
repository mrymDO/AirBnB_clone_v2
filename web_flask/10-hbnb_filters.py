#!/usr/bin/python3
""" start flask app """

from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """ remove sql session """
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """ display hbnb_filters """
    state_objects = storage.all('State').values()
    states = sorted(state_objects, key=lambda state: state.name)

    amenities_objects = storage.all('Amenity').values()
    amenities = sorted(amenities_objects, key=lambda amenity: amenity.name)

    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port='5000', debug=True)
