from sqlalchemy import Column, Integer, String, DateTime

from app.models import Base


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime)
    is_superuser = Column(Integer, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Integer, nullable=False)
    is_active = Column(Integer, nullable=False)
    date_joined = Column(DateTime, nullable=False)
