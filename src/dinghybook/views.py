from flask import render_template

from dinghybook import app


@app.route('/')
def index():
    return render_template('index.html.j2')


@app.route('/boats/')
@app.route('/boats/<int:boat_id>')
def boat(boat_id=None):
    if boat_id:
        return f'Boat {boat_id} selected!'
    return 'All the boats!'
