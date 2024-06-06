from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base  # , scoped_session, sessionmaker

Base = declarative_base()
db = SQLAlchemy(model_class=Base)
