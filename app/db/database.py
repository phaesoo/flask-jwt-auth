from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


db_sessions = dict()
db_engines = dict()


def init_db():
    db_name = "auth"
    engine = create_engine("sqlite:///auth.db", echo=True)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )

    # import models
    from app.models import Base
    from app.models import auth

    Base.query = db_session.query_property()
    Base.metadata.create_all(engine)
    
    db_sessions[db_name] = db_session
    db_engines[db_name] = engine
    

def get_session(db_name):
    session = db_sessions.get(db_name)
    if session is None:
        raise ValueError("Invalid DB Name: {}".format(db_name))
    return session


def get_engine(db_name):
    engine = db_engines.get(db_name)
    if engine is None:
        raise ValueError("Invalid DB Name: {}".format(db_name))
    return engine