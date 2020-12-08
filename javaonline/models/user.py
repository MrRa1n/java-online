from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

from javaonline.db.base import Base, Session
from javaonline.models.role import Role
from javaonline.models.challenge import Challenge

from javaonline.app import login_manager

session = Session()

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))

user_roles_association = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('role_id', Integer, ForeignKey('roles.role_id'))
)

user_challenge_association = Table(
    'users_challenges', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('challenge_id', Integer, ForeignKey('challenges.challenge_id'))
)

class User(UserMixin, Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    avatar_url = Column(String, nullable=False)
    experience_points = Column(Integer, nullable=False)
    created_on = Column(Date, nullable=False)
    last_login = Column(Date, nullable=True)
    roles = relationship('Role', secondary=user_roles_association)
    challenges = relationship('Challenge', secondary=user_challenge_association)

    def __init__(self, username, password, email, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.avatar_url = None
        self.experience_points = 0
        self.last_login = None
        self.roles = []
        self.challenges = []

    def set_experience_points(self, xp):
        self.experience_points = xp

    def set_created_on(self, date):
        self.created_on = date

    def set_last_login(self, date):
        self.last_login = date

    def __repr__(self):
        return '<User {}, {}>'.format(self.username, self.roles)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
           return (self.user_id)

