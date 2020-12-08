from sqlalchemy import Column, Integer, String

from javaonline.db.base import Base

class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, nullable=False, primary_key=True)
    role_name = Column(String, nullable=False)

    def __init__(self, name):
        self.role_name = name

    def __repr__(self):
        return '<Role {}>'.format(self.role_name)