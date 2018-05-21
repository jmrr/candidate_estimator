from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Boolean, DateTime, Text, Integer, Float

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)


class Candidates(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    applicationId = Column(Text)
    candidateId = Column(Integer)
    isRetake = Column(Boolean)
    invitationDate = Column(DateTime)
    applicationTime = Column(DateTime)
    speechToText = Column(Text)
    videoLength = Column(Float)
    score = Column(Integer)
    predictedScore = Column(Integer)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
