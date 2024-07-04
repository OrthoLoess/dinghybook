# SPDX-FileCopyrightText: 2024-present Ed Landamore <ortho@ratship.net>
#
# SPDX-License-Identifier: MIT
import tomllib
from dotenv import load_dotenv
from flask import Flask
from flask_bootstrap import Bootstrap5

# from flask_talisman import Talisman
from dinghybook.database import db

load_dotenv()
app = Flask(__name__)
app.config.from_file('config.toml', load=tomllib.load, text=False)
app.config.from_prefixed_env()

# Talisman(app)
bootstrap = Bootstrap5(app)

import dinghybook.models
import dinghybook.views

# db.create_all()
db.init_app(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
