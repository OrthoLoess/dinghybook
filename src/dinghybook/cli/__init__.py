# SPDX-FileCopyrightText: 2024-present Ed Landamore <ortho@ratship.net>
#
# SPDX-License-Identifier: MIT
import os

import click
import tomllib

from dinghybook import app
from dinghybook.__about__ import __version__
from dinghybook.database import db
from dinghybook.models import Boat, Handicap, Issue, Type, User


@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name='dinghybook')
def dinghybook():
    pass


@dinghybook.command()
@click.option('-s', '--sample-data', is_flag=True)
def initdb(sample_data):
    if sample_data:
        # load sample data from toml
        with open(os.path.join(app.instance_path, 'sample.toml'), 'rb') as f:
            data = tomllib.load(f)

        with app.app_context():
            db.create_all()
            for datum in data['users']:
                obj = User()
                for prop in datum:
                    setattr(obj, prop, datum[prop])
                db.session.add(obj)
            db.session.commit()
            for datum in data['boats']:
                obj = Boat()
                for prop in datum:
                    setattr(obj, prop, datum[prop])
                db.session.add(obj)
            db.session.commit()
            for datum in data['types']:
                obj = Type()
                for prop in datum:
                    setattr(obj, prop, datum[prop])
                db.session.add(obj)
            db.session.commit()
            for datum in data['handicaps']:
                obj = Handicap()
                for prop in datum:
                    setattr(obj, prop, datum[prop])
                db.session.add(obj)
            db.session.commit()
            for datum in data['issues']:
                obj = Issue()
                for prop in datum:
                    setattr(obj, prop, datum[prop])
                db.session.add(obj)
            db.session.commit()
        click.echo('Initialized the database with sample data')
    else:
        with app.app_context():
            db.create_all()
        click.echo('Initialized the database')


@dinghybook.command()
def dropdb():
    with app.app_context():
        db.drop_all()
    click.echo('Dropped the database')
