from flask import render_template

from dinghybook import app
from dinghybook.database import db
from dinghybook.models import Boat, Event, Handicap, Issue, Type


@app.route('/')
def index():
    # db.create_all()
    return render_template('index.html.j2')


@app.route('/boats/')
def boats():
    boats_tmp = db.session.execute(db.select(Boat)).scalars()
    boats = [
        {
            'id': boat.id,
            'name': boat.name,
            'type': boat.type.name,
            'last_updated': boat.last_updated.strftime('%d/%m/%Y, %H:%M:%S'),
        }
        for boat in boats_tmp.all()
    ]
    return render_template('list.html.j2', list=boats)


@app.route('/boats/<int:boat_id>')
def boat(boat_id=None):
    if boat_id:
        return f'Boat {boat_id} selected!'
    return 'All the boats!'


@app.route('/classes/')
def types():
    tmp = db.session.execute(db.select(Type)).scalars()
    things = [
        {
            'id': thing.id,
            'name': thing.name,
            'description': thing.description,
        }
        for thing in tmp.all()
    ]
    return render_template('list.html.j2', list=things)


@app.route('/handicaps/')
def handicaps():
    tmp = db.session.execute(db.select(Handicap)).scalars()
    things = []
    for thing in tmp.all():
        timestring = thing.effective_from.strftime('%d/%m/%Y, %H:%M:%S') if thing.effective_from else ''
        things.append({
            'id': thing.id,
            'value': thing.value,
            'type': thing.type.name,
            'effective_from': timestring,
            'comment': thing.comment or '',
        })
    return render_template('list.html.j2', list=things)


@app.route('/issues/')
def issues():
    tmp = db.session.execute(db.select(Issue)).scalars()
    things = [
        {
            'id': thing.id,
            'type': thing.type.name or '',
            'boat': thing.boat.name or '',
            'reported': thing.reported.strftime('%d/%m/%Y, %H:%M:%S'),
            'comment': thing.comment or '',
            'more_details': thing.more_details or '',
        }
        for thing in tmp.all()
    ]
    return render_template('list.html.j2', list=things)


@app.route('/events/')
def events():
    tmp = db.session.execute(db.select(Event)).scalars()
    things = [
        {
            'id': thing.id,
            'type': thing.type.name or '',
            'date': thing.date.strftime('%d/%m/%Y') or '',
        }
        for thing in tmp.all()
    ]
    return render_template('list.html.j2', list=things)
