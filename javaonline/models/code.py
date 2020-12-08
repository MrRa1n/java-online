from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from javaonline.db.base import Base

class Code(Base):
    __tablename__ = 'code'

    code_id = Column(Integer, primary_key=True)
    code_url = Column(String)
    type = Column(String, nullable=False)
    challenge_id = Column(Integer, ForeignKey('challenges.challenge_id'))
    challenge = relationship('Challenge', backref='code')

    def __init__(self, url, type, challenge):
        self.code_url = url
        self.type = type
        self.challenge = challenge
