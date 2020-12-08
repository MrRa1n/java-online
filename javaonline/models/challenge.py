from sqlalchemy import Column, String, Integer

from javaonline.db.base import Base, Session

session = Session()

class Challenge(Base):
    __tablename__ = 'challenges'

    challenge_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    instructions = Column(String, nullable=False)

    def __init__(self, title, instructions):
        self.title = title
        self.instructions = instructions
