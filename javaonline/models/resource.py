from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from javaonline.db.base import Base

class Resource(Base):
    __tablename__ = 'resources'

    resource_id = Column(Integer, primary_key=True)
    resource_url = Column(String)
    challenge_id = Column(Integer, ForeignKey('challenges.challenge_id'))
    challenge = relationship('Challenge', backref='resources')

    def __init__(self, url, challenge):
        self.code_url = url
        self.challenge = challenge
