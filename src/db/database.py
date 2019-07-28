from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


db_sessions = dict()
db_engines = dict()

def init_db():
    db_name = "auth"
    engine = create_engine("sqlite:///auth.db", echo=True)
    db_sessions[db_name] = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )
    
    db_engines[db_name] = engine
    

def get_session(db_name):
    session = db_sessions.get(db_name)
    if session is None:
        raise ValueError("Invalid DB Name: {}".format(db_name))
    return session